import pytest
from app.state import create_initial_state
from app.graph.workflow import (
    rollback_and_reroute_with_feedback,
    approve_and_apply,
)


def test_checkpointer_pause_at_hitl_gate(fresh_graph):
    """
    Assert that the graph executes fetch, lint, and propose_refactor,
    and pauses execution before apply_changes_node.
    """
    config = {"configurable": {"thread_id": "test-pause-gate"}}
    initial_state = create_initial_state(
        pr_url="https://github.com/test-owner/test-repo/pull/1",
        initial_code="def run():\n  x=1\n  return x\n",
    )

    fresh_graph.invoke(initial_state, config)
    snapshot = fresh_graph.get_state(config)

    # Assert graph is halted right before the write node
    assert snapshot.next == ("apply_changes_node",)
    assert snapshot.values["code_contents"] != ""
    assert snapshot.values["refactored_code"] != ""
    assert snapshot.values["is_approved"] is False


def test_checkpointer_rollback_and_reroute_assertions(fresh_graph):
    """
    Checkpointer Rollback Assertions:
    Mock reviewer responses and assert the graph successfully rolls back to the
    refactor generation node upon rejection with feedback.
    """
    config = {"configurable": {"thread_id": "test-rollback-reroute"}}
    initial_state = create_initial_state(
        pr_url="https://github.com/test-owner/test-repo/pull/5",
        initial_code=(
            "def calculate_total_price(items, tax_rate):\n"
            "    total = 0\n"
            "    for item in items:\n"
            "        total = total + item['price']\n"
            "    return total * (1 + tax_rate)\n"
        ),
    )

    fresh_graph.invoke(initial_state, config)
    state_before_review = fresh_graph.get_state(config)
    assert state_before_review.next == ("apply_changes_node",)

    # 1. Reviewer rejects and requests list comprehensions
    feedback_str = "Use list comprehensions instead of loops"
    updated_state = rollback_and_reroute_with_feedback(
        fresh_graph, config, feedback=feedback_str
    )

    # 2. Assert state updated with feedback and graph re-evaluated propose_refactor_node
    assert updated_state["reviewer_feedback"] == feedback_str
    assert updated_state["is_approved"] is False
    assert "list comprehension" in updated_state["refactored_code"].lower()

    # 3. Assert graph has paused again at the approval checkpoint
    state_after_reroute = fresh_graph.get_state(config)
    assert state_after_reroute.next == ("apply_changes_node",)


def test_approval_pathway_commits_and_completes(fresh_graph):
    """
    Assert that approving resumes the graph, executes apply_changes_node,
    and terminates the thread at END.
    """
    config = {"configurable": {"thread_id": "test-approval-complete"}}
    initial_state = create_initial_state(
        pr_url="https://github.com/test-owner/test-repo/pull/8",
        initial_code="def hello():\n    return 'world'\n",
    )

    fresh_graph.invoke(initial_state, config)
    assert fresh_graph.get_state(config).next == ("apply_changes_node",)

    # Approve
    final_state = approve_and_apply(fresh_graph, config, feedback="LGTM")

    # Assert thread completed and changes were committed
    state_after_approval = fresh_graph.get_state(config)
    assert state_after_approval.next == ()
    assert final_state["is_approved"] is True
    assert final_state["commit_sha"] is not None
    assert final_state["status"] == "changes_committed"


def test_history_audit_trail_recorded(fresh_graph):
    """Verify that every transition records audit entries in state history."""
    config = {"configurable": {"thread_id": "test-audit-trail"}}
    initial_state = create_initial_state(
        pr_url="https://github.com/test-owner/test-repo/pull/9"
    )

    fresh_graph.invoke(initial_state, config)
    history = fresh_graph.get_state(config).values["history"]
    node_names = [h["node"] for h in history]

    assert "initialize" in node_names
    assert "fetch_pr_node" in node_names
    assert "lint_code_node" in node_names
    assert "propose_refactor_node" in node_names
