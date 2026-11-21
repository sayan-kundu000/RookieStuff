import pytest
from fastapi.testclient import TestClient


def test_health_check_endpoint(client: TestClient):
    """Assert health check responds with 200 OK and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "checkpointer" in data


def test_root_endpoint_metadata(client: TestClient):
    """Assert root endpoint returns RookieStuff application metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "RookieStuff"
    assert "documentation" in data


def test_case_1_webhook_pr_ingestion_and_pause_gate(client: TestClient):
    """
    Verification Test Case 1: Webhook PR Ingestion, Linting, & HITL Pause Gate
    1. Start FastAPI server.
    2. Simulate GitHub PR webhook event by posting mock payload containing repository URL and branch.
    3. Verify server creates new thread, fetches files, executes sandbox linter, and halts at approval checkpoint.
    """
    payload = {
        "repository_url": "https://github.com/octocat/Hello-World",
        "branch": "feature/refactor-pricing",
        "pr_url": "https://github.com/octocat/Hello-World/pull/42",
        "code_contents": (
            "def calculate_total_price(items, tax_rate):\n"
            "    total = 0\n"
            "    for item in items:\n"
            "      total = total + item['price']\n"
            "    tax=total*tax_rate\n"
            "    return total+tax\n"
        ),
    }

    response = client.post("/api/webhooks/github", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "thread_id" in data
    assert data["status"] == "paused_at_approval_checkpoint"
    assert data["next_nodes"] == ["apply_changes_node"]
    assert data["refactored_code"] is not None
    assert data["lint_errors"] is not None


def test_case_2_feedback_input_and_reroute_loop(client: TestClient):
    """
    Verification Test Case 2: Feedback Input & Refactoring Proposal Re-route Loop
    1. Post review rejection to /api/reviews/{thread_id}/approve with approved=false and feedback='Use list comprehensions instead of loops'.
    2. Verify agent re-runs refactoring proposal node using feedback, updates draft, and pauses again at write gate.
    """
    # 1. Ingest webhook to create active thread
    wh_res = client.post(
        "/api/webhooks/github",
        json={
            "repository_url": "https://github.com/octocat/Hello-World",
            "branch": "feature/reroute-test",
            "pr_url": "https://github.com/octocat/Hello-World/pull/99",
        },
    )
    thread_id = wh_res.json()["thread_id"]

    # 2. Post review rejection
    reject_payload = {
        "approved": False,
        "feedback": "Use list comprehensions instead of loops",
    }
    reject_res = client.post(f"/api/reviews/{thread_id}/approve", json=reject_payload)
    assert reject_res.status_code == 200

    data = reject_res.json()
    assert data["is_approved"] is False
    assert data["status"] == "feedback_applied_awaiting_approval"
    assert data["reviewer_feedback"] == "Use list comprehensions instead of loops"
    # Verify agent updated draft with list comprehension
    assert "list comprehension" in data["refactored_code"].lower()
    # Verify paused again at write gate
    assert data["next_nodes"] == ["apply_changes_node"]


def test_case_3_approval_and_commit_writeback(client: TestClient):
    """
    Verification Test Case 3: Approval and Git commit write back
    1. Post approval payload containing approved=true to /api/reviews/{thread_id}/approve.
    2. Verify agent resumes, runs applyChanges node, commits code to branch, and completes thread.
    """
    # 1. Create thread via webhook
    wh_res = client.post(
        "/api/webhooks/github",
        json={
            "repository_url": "https://github.com/octocat/Hello-World",
            "branch": "feature/commit-test",
            "pr_url": "https://github.com/octocat/Hello-World/pull/101",
        },
    )
    thread_id = wh_res.json()["thread_id"]

    # 2. Approve PR
    approval_payload = {
        "approved": True,
        "feedback": "Code looks clean and passes review.",
    }
    appr_res = client.post(f"/api/reviews/{thread_id}/approve", json=approval_payload)
    assert appr_res.status_code == 200

    data = appr_res.json()
    assert data["is_approved"] is True
    assert data["status"] == "completed"
    assert data["commit_sha"] is not None
    assert data["next_nodes"] == []


def test_inspect_review_state_details(client: TestClient):
    """Assert GET /api/reviews/{thread_id} returns state details and history."""
    wh_res = client.post(
        "/api/webhooks/github",
        json={"pr_url": "https://github.com/octocat/Hello-World/pull/555"},
    )
    thread_id = wh_res.json()["thread_id"]

    state_res = client.get(f"/api/reviews/{thread_id}")
    assert state_res.status_code == 200
    state_data = state_res.json()
    assert state_data["thread_id"] == thread_id
    assert len(state_data["history"]) >= 3


def test_approve_nonexistent_thread_returns_404(client: TestClient):
    """Assert approving unknown thread returns 404 Not Found."""
    res = client.post(
        "/api/reviews/non-existent-thread/approve",
        json={"approved": True},
    )
    assert res.status_code == 404
