import pytest
from fastapi.testclient import TestClient
from langgraph.checkpoint.memory import MemorySaver

from main import app
from app.graph.workflow import build_review_graph


@pytest.fixture(scope="session")
def client():
    """Provides a FastAPI test client for API endpoint integration tests."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def fresh_graph():
    """Provides an isolated review graph with fresh in-memory checkpointer for unit tests."""
    checkpointer = MemorySaver()
    return build_review_graph(checkpointer=checkpointer)
