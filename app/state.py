import datetime
from typing import TypedDict, Optional, List, Dict, Any


class ReviewState(TypedDict, total=False):
    """
    LangGraph state schema for RookieStuff review pipeline.
    Contains all required keys:
    - pr_url: str
    - code_contents: str
    - lint_errors: str
    - refactored_code: str
    - is_approved: bool
    - reviewer_feedback: Optional[str]
    - history: list
    """

    # Core required keys
    pr_url: str
    code_contents: str
    lint_errors: str
    refactored_code: str
    is_approved: bool
    reviewer_feedback: Optional[str]
    history: List[Dict[str, Any]]

    # Repository & PR context metadata
    repo_name: Optional[str]
    pr_number: Optional[int]
    file_path: Optional[str]
    branch_name: Optional[str]
    commit_sha: Optional[str]
    status: Optional[str]


def create_initial_state(
    pr_url: str,
    repo_name: Optional[str] = None,
    pr_number: Optional[int] = None,
    branch_name: Optional[str] = None,
    file_path: Optional[str] = None,
    initial_code: Optional[str] = None,
) -> ReviewState:
    """Helper to initialize a clean ReviewState dictionary."""
    return {
        "pr_url": pr_url,
        "code_contents": initial_code or "",
        "lint_errors": "",
        "refactored_code": "",
        "is_approved": False,
        "reviewer_feedback": None,
        "history": [
            {
                "node": "initialize",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "message": f"Initialized review session for PR: {pr_url}",
            }
        ],
        "repo_name": repo_name,
        "pr_number": pr_number,
        "branch_name": branch_name,
        "file_path": file_path,
        "commit_sha": None,
        "status": "initialized",
    }


def add_history_entry(
    history: Optional[List[Dict[str, Any]]],
    node: str,
    action: str,
    details: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Helper to append an audit entry to history."""
    entries = list(history) if history else []
    entries.append(
        {
            "node": node,
            "action": action,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "details": details or {},
        }
    )
    return entries
