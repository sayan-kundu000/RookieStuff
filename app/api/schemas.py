from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class GitHubWebhookPayload(BaseModel):
    """
    Flexible GitHub Webhook payload schema.
    Supports both standard GitHub webhook events (action, pull_request, repository)
    and streamlined direct testing payloads (repository_url, branch, pr_url).
    """

    # Direct testing fields
    repository_url: Optional[str] = Field(None, description="Repository URL or target PR URL")
    branch: Optional[str] = Field(None, description="Branch name under review")
    pr_url: Optional[str] = Field(None, description="Explicit Pull Request URL")
    code_contents: Optional[str] = Field(None, description="Optional raw code for testing")

    # Standard GitHub webhook event fields
    action: Optional[str] = Field(None, description="GitHub event action (opened, synchronize)")
    number: Optional[int] = Field(None, description="PR number")
    pull_request: Optional[Dict[str, Any]] = Field(None, description="Full GitHub PR object")
    repository: Optional[Dict[str, Any]] = Field(None, description="Full GitHub repository object")

    model_config = {
        "json_schema_extra": {
            "example": {
                "repository_url": "https://github.com/octocat/Hello-World",
                "branch": "feature/refactor",
                "pr_url": "https://github.com/octocat/Hello-World/pull/42",
            }
        }
    }


class ApprovalPayload(BaseModel):
    """Payload for human approval / rejection decisions."""

    approved: bool = Field(..., description="Approval status: true to apply, false to re-route")
    feedback: Optional[str] = Field(
        None, description="Optional reviewer feedback/instructions for refactoring"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "approved": False,
                "feedback": "Use list comprehensions instead of loops",
            }
        }
    }


class WebhookResponse(BaseModel):
    """Response returned upon PR webhook ingestion."""

    thread_id: str
    status: str
    pr_url: str
    branch_name: Optional[str]
    lint_errors: Optional[str]
    refactored_code: Optional[str]
    next_nodes: List[str]
    message: str


class ReviewResponse(BaseModel):
    """Response returned upon review decision submission."""

    thread_id: str
    is_approved: bool
    status: str
    reviewer_feedback: Optional[str]
    refactored_code: Optional[str]
    commit_sha: Optional[str]
    next_nodes: List[str]
    message: str


class ReviewStateDetail(BaseModel):
    """Detailed inspection of a review thread state."""

    thread_id: str
    pr_url: Optional[str]
    status: Optional[str]
    is_approved: Optional[bool]
    reviewer_feedback: Optional[str]
    lint_errors: Optional[str]
    refactored_code: Optional[str]
    code_contents: Optional[str]
    commit_sha: Optional[str]
    history: List[Dict[str, Any]]
    next_nodes: List[str]
