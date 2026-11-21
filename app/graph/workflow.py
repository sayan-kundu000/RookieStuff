import logging
from typing import Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver

from app.config import get_settings
from app.state import ReviewState, add_history_entry
from app.graph.nodes import (
    fetch_pr_node,
    lint_code_node,
    propose_refactor_node,
    apply_changes_node,
)

logger = logging.getLogger("rookiestuff.workflow")

# Global checkpointer instance for application lifetime
_GLOBAL_CHECKPOINTER: Optional[BaseCheckpointSaver] = None


def get_checkpointer(checkpointer_type: Optional[str] = None) -> BaseCheckpointSaver:
    """Return configured checkpointer (MemorySaver or SqliteSaver)."""
    global _GLOBAL_CHECKPOINTER
    if _GLOBAL_CHECKPOINTER is not None:
        return _GLOBAL_CHECKPOINTER

    settings = get_settings()
    c_type = checkpointer_type or settings.checkpointer_type

    if c_type == "sqlite":
        try:
            import sqlite3
            from langgraph.checkpoint.sqlite import SqliteSaver

            conn = sqlite3.connect(settings.sqlite_db_path, check_same_thread=False)
            _GLOBAL_CHECKPOINTER = SqliteSaver(conn)
            logger.info(f"Initialized SqliteSaver checkpointer at {settings.sqlite_db_path}")
            return _GLOBAL_CHECKPOINTER
        except Exception as exc:
            logger.warning(f"Failed to initialize SqliteSaver: {exc}. Defaulting to MemorySaver.")

    _GLOBAL_CHECKPOINTER = MemorySaver()
    logger.info("Initialized in-memory MemorySaver checkpointer.")
    return _GLOBAL_CHECKPOINTER


def build_review_graph(
    checkpointer: Optional[BaseCheckpointSaver] = None,
    interrupt_before: Optional[List[str]] = None,
):
    """
    Constructs and compiles the RookieStuff review pipeline graph.
    Configures persistent checkpoints and human-in-the-loop (HITL) interrupt gates.
    """
    if checkpointer is None:
        checkpointer = get_checkpointer()

    if interrupt_before is None:
        # Halt execution right before write node for human validation
        interrupt_before = ["apply_changes_node"]

    builder = StateGraph(ReviewState)

    # 1. Add core nodes
    builder.add_node("fetch_pr_node", fetch_pr_node)
    builder.add_node("lint_code_node", lint_code_node)
    builder.add_node("propose_refactor_node", propose_refactor_node)
    builder.add_node("apply_changes_node", apply_changes_node)

    # 2. Add sequential review edges
    builder.add_edge(START, "fetch_pr_node")
    builder.add_edge("fetch_pr_node", "lint_code_node")
    builder.add_edge("lint_code_node", "propose_refactor_node")
    builder.add_edge("propose_refactor_node", "apply_changes_node")
    builder.add_edge("apply_changes_node", END)

    # Compile with persistent checkpointing and HITL interrupt gate
    graph = builder.compile(
        checkpointer=checkpointer,
        interrupt_before=interrupt_before,
    )
    return graph


# Singleton compiled graph instance for the app
review_graph = build_review_graph()


def rollback_and_reroute_with_feedback(
    graph,
    config: Dict[str, Any],
    feedback: str,
) -> Dict[str, Any]:
    """
    Human Review Feedback Loop:
    1. Writes feedback to graph checkpointer state.
    2. Rewinds/re-routes the thread to propose_refactor_node (via as_node='lint_code_node').
    3. Re-runs the LLM propose_refactor_node with the feedback.
    4. Halts again at the approval checkpoint (interrupt_before=['apply_changes_node']).
    """
    state_snapshot = graph.get_state(config)
    current_history = state_snapshot.values.get("history", [])

    updated_history = add_history_entry(
        current_history,
        node="human_review_gate",
        action="rejected_with_feedback",
        details={"feedback": feedback},
    )

    # Re-route to propose_refactor_node by setting as_node="lint_code_node"
    graph.update_state(
        config,
        {
            "is_approved": False,
            "reviewer_feedback": feedback,
            "status": "feedback_received",
            "history": updated_history,
        },
        as_node="lint_code_node",
    )

    # Resume graph: executes propose_refactor_node and pauses again before apply_changes_node
    graph.invoke(None, config)
    return graph.get_state(config).values


def approve_and_apply(
    graph,
    config: Dict[str, Any],
    feedback: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Human Review Approval:
    1. Updates checkpointer state with is_approved=True.
    2. Resumes graph execution to run apply_changes_node and commit back to GitHub.
    """
    state_snapshot = graph.get_state(config)
    current_history = state_snapshot.values.get("history", [])

    updated_history = add_history_entry(
        current_history,
        node="human_review_gate",
        action="approved",
        details={"feedback": feedback or "Approved without additional comments"},
    )

    graph.update_state(
        config,
        {
            "is_approved": True,
            "reviewer_feedback": feedback,
            "status": "approved",
            "history": updated_history,
        },
    )

    # Resume graph: runs apply_changes_node and completes at END
    graph.invoke(None, config)
    return graph.get_state(config).values
