import uuid
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Body

from app.api.schemas import (
    GitHubWebhookPayload,
    ApprovalPayload,
    WebhookResponse,
    ReviewResponse,
    ReviewStateDetail,
)
from app.state import create_initial_state
from app.graph.workflow import (
    review_graph,
    rollback_and_reroute_with_feedback,
    approve_and_apply,
)

logger = logging.getLogger("rookiestuff.api")
router = APIRouter(prefix="/api", tags=["Code Review"])


def extract_pr_info(payload: Optional[GitHubWebhookPayload]) -> Dict[str, Any]:
    """Normalize PR info from either full GitHub webhooks or direct test payloads."""
    if payload is None:
        payload = GitHubWebhookPayload()

    pr_url = payload.pr_url
    branch_name = payload.branch
    repo_name = None
    pr_number = payload.number

    # GitHub standard webhook structure
    if payload.pull_request:
        pr_obj = payload.pull_request
        pr_url = pr_url or pr_obj.get("html_url")
        if not branch_name and "head" in pr_obj:
            branch_name = pr_obj["head"].get("ref")
        pr_number = pr_number or pr_obj.get("number")

    if payload.repository:
        repo_obj = payload.repository
        repo_name = repo_obj.get("full_name") or repo_obj.get("name")
        if not pr_url and payload.repository_url:
            pr_url = payload.repository_url

    # Direct test payload fallbacks
    if not pr_url and payload.repository_url:
        pr_url = payload.repository_url
        if "/pull/" not in pr_url:
            pr_url = f"{pr_url.rstrip('/')}/pull/{pr_number or 1}"

    if not pr_url:
        pr_url = "https://github.com/mock-owner/mock-repo/pull/1"

    return {
        "pr_url": pr_url,
        "branch_name": branch_name or "main",
        "repo_name": repo_name,
        "pr_number": pr_number or 1,
        "code_contents": payload.code_contents,
    }


@router.post(
    "/webhooks/github",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest GitHub PR Webhook",
    description="Receives Pull Request event payloads, extracts parameters, and executes the LangGraph review pipeline up to the HITL approval gate.",
)
async def github_webhook(payload: Optional[GitHubWebhookPayload] = Body(default=None)):
    """
    POST /api/webhooks/github
    1. Extracts PR URL and repository details (with safe fallback if payload is empty).
    2. Initializes a new LangGraph thread.
    3. Runs pipeline: fetch_pr_node -> lint_code_node -> propose_refactor_node.
    4. Halts at interrupt_before=['apply_changes_node'] waiting for human validation.
    """
    try:
        pr_info = extract_pr_info(payload)
        thread_id = f"review-{uuid.uuid4().hex[:12]}"
        config = {"configurable": {"thread_id": thread_id}}

        logger.info(f"Triggering LangGraph review thread {thread_id} for PR {pr_info['pr_url']}")

        initial_state = create_initial_state(
            pr_url=pr_info["pr_url"],
            repo_name=pr_info["repo_name"],
            pr_number=pr_info["pr_number"],
            branch_name=pr_info["branch_name"],
            initial_code=pr_info.get("code_contents"),
        )

        # Executes until HITL interrupt gate before apply_changes_node
        review_graph.invoke(initial_state, config)

        current_snapshot = review_graph.get_state(config)
        values = current_snapshot.values
        next_nodes = list(current_snapshot.next)

        return WebhookResponse(
            thread_id=thread_id,
            status="paused_at_approval_checkpoint",
            pr_url=values.get("pr_url", pr_info["pr_url"]),
            branch_name=values.get("branch_name"),
            lint_errors=values.get("lint_errors"),
            refactored_code=values.get("refactored_code"),
            next_nodes=next_nodes,
            message="Review pipeline completed linting and refactor proposal. Paused at approval checkpoint.",
        )
    except Exception as exc:
        logger.error(f"Graph execution failed during webhook ingestion: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Graph execution error: {str(exc)}",
        )


@router.post(
    "/reviews/{thread_id}/approve",
    response_model=ReviewResponse,
    summary="Submit Human Review Decision",
    description="Accepts approval payloads (approved: true/false and optional feedback). Re-routes to refactor on rejection or commits code on approval.",
)
async def submit_review_decision(thread_id: str, payload: ApprovalPayload):
    """
    POST /api/reviews/{thread_id}/approve
    - If approved == False: Writes feedback to state, rolls back to propose_refactor_node, regenerates proposal, and halts again at approval gate.
    - If approved == True: Updates state to approved, resumes graph, executes apply_changes_node, commits changes, and completes thread.
    """
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = review_graph.get_state(config)

    if not snapshot or not snapshot.values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review thread '{thread_id}' not found in checkpointer.",
        )

    if not snapshot.next and snapshot.values.get("status") == "changes_committed":
        return ReviewResponse(
            thread_id=thread_id,
            is_approved=True,
            status="completed",
            reviewer_feedback=snapshot.values.get("reviewer_feedback"),
            refactored_code=snapshot.values.get("refactored_code"),
            commit_sha=snapshot.values.get("commit_sha"),
            next_nodes=[],
            message="This review thread has already been approved and committed.",
        )

    try:
        if not payload.approved:
            # Rejection with feedback -> rollback/re-route to propose_refactor_node
            updated_state = rollback_and_reroute_with_feedback(
                review_graph,
                config,
                payload.feedback or "Please revise refactored draft to fix lint and stylistic errors.",
            )
            next_snapshot = review_graph.get_state(config)
            return ReviewResponse(
                thread_id=thread_id,
                is_approved=False,
                status="feedback_applied_awaiting_approval",
                reviewer_feedback=updated_state.get("reviewer_feedback"),
                refactored_code=updated_state.get("refactored_code"),
                commit_sha=None,
                next_nodes=list(next_snapshot.next),
                message="Reviewer feedback applied. Regenerated refactoring proposal and paused at approval gate.",
            )
        else:
            # Approval -> execute apply_changes_node and finish
            updated_state = approve_and_apply(review_graph, config, payload.feedback)
            next_snapshot = review_graph.get_state(config)
            return ReviewResponse(
                thread_id=thread_id,
                is_approved=True,
                status="completed",
                reviewer_feedback=updated_state.get("reviewer_feedback"),
                refactored_code=updated_state.get("refactored_code"),
                commit_sha=updated_state.get("commit_sha"),
                next_nodes=list(next_snapshot.next),
                message="Approved. Changes committed to repository branch successfully.",
            )
    except Exception as exc:
        logger.error(f"Error handling approval decision for thread {thread_id}: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process review decision: {str(exc)}",
        )


@router.get(
    "/reviews/{thread_id}",
    response_model=ReviewStateDetail,
    summary="Get Review Session State",
    description="Inspect current state, audit history, and next scheduled node for a review session thread.",
)
async def get_review_state(thread_id: str):
    """Retrieve full review state and history for a given thread."""
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = review_graph.get_state(config)

    if not snapshot or not snapshot.values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review thread '{thread_id}' not found.",
        )

    values = snapshot.values
    return ReviewStateDetail(
        thread_id=thread_id,
        pr_url=values.get("pr_url"),
        status=values.get("status"),
        is_approved=values.get("is_approved"),
        reviewer_feedback=values.get("reviewer_feedback"),
        lint_errors=values.get("lint_errors"),
        refactored_code=values.get("refactored_code"),
        code_contents=values.get("code_contents"),
        commit_sha=values.get("commit_sha"),
        history=values.get("history", []),
        next_nodes=list(snapshot.next),
    )
