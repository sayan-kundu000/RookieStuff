import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import router as api_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("rookiestuff")


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RookieStuff - Autonomous Code Review & Refactoring Agent</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0d1117;
      --card-bg: #161b22;
      --border-color: #30363d;
      --text-main: #c9d1d9;
      --text-muted: #8b949e;
      --accent: #58a6ff;
      --accent-green: #238636;
      --accent-green-hover: #2ea043;
      --accent-red: #da3633;
      --accent-red-hover: #f85149;
      --accent-amber: #d29922;
      --code-bg: #090d13;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 60px;
    }
    header {
      background-color: var(--card-bg);
      border-bottom: 1px solid var(--border-color);
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, #238636, #58a6ff);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: white;
      font-size: 18px;
    }
    .brand-title {
      font-size: 18px;
      font-weight: 700;
      color: #f0f6fc;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tag {
      font-size: 11px;
      background-color: rgba(88, 166, 255, 0.15);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 12px;
      border: 1px solid rgba(88, 166, 255, 0.3);
      font-weight: 500;
    }
    .nav-links {
      display: flex;
      gap: 16px;
      align-items: center;
    }
    .nav-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      transition: color 0.2s;
    }
    .nav-links a:hover { color: var(--accent); }
    .container {
      max-width: 1280px;
      margin: 24px auto;
      padding: 0 20px;
    }
    .grid {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 20px;
    }
    @media (max-width: 960px) {
      .grid { grid-template-columns: 1fr; }
    }
    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .card-title {
      font-size: 15px;
      font-weight: 600;
      color: #f0f6fc;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .form-group {
      margin-bottom: 14px;
    }
    label {
      display: block;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    input, textarea {
      width: 100%;
      background-color: var(--code-bg);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 8px 12px;
      color: #f0f6fc;
      font-size: 13px;
      font-family: 'Inter', sans-serif;
      transition: border-color 0.2s;
    }
    textarea {
      font-family: 'Fira Code', monospace;
      font-size: 12px;
      resize: vertical;
    }
    input:focus, textarea:focus {
      outline: none;
      border-color: var(--accent);
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background-color: var(--accent-green);
      color: white;
      width: 100%;
    }
    .btn-primary:hover { background-color: var(--accent-green-hover); }
    .btn-danger {
      background-color: var(--accent-red);
      color: white;
    }
    .btn-danger:hover { background-color: var(--accent-red-hover); }
    .btn-success {
      background-color: var(--accent-green);
      color: white;
    }
    .btn-success:hover { background-color: var(--accent-green-hover); }
    .code-box {
      background-color: var(--code-bg);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
      font-family: 'Fira Code', monospace;
      font-size: 12px;
      color: #e6edf3;
      white-space: pre-wrap;
      overflow-x: auto;
      max-height: 280px;
    }
    .status-badge {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
    }
    .status-paused { background-color: rgba(210, 153, 34, 0.2); color: var(--accent-amber); border: 1px solid var(--accent-amber); }
    .status-committed { background-color: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid #3fb950; }
    .diff-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }
    @media (max-width: 800px) {
      .diff-container { grid-template-columns: 1fr; }
    }
    .feedback-panel {
      margin-top: 16px;
      padding: 16px;
      background-color: rgba(88, 166, 255, 0.05);
      border: 1px solid rgba(88, 166, 255, 0.2);
      border-radius: 8px;
    }
    .history-list {
      margin-top: 12px;
      font-size: 12px;
      max-height: 180px;
      overflow-y: auto;
    }
    .history-item {
      padding: 6px 0;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
    }
    .history-item strong { color: var(--text-main); }
    .loader {
      display: none;
      width: 16px;
      height: 16px;
      border: 2px solid #ffffff;
      border-top: 2px solid transparent;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>

<header>
  <div class="brand">
    <div class="brand-logo">R</div>
    <div class="brand-title">
      RookieStuff
      <span class="tag">LangGraph Agent</span>
    </div>
  </div>
  <div class="nav-links">
    <a href="/docs" target="_blank">Swagger API</a>
    <a href="/redoc" target="_blank">ReDoc</a>
    <a href="/openapi.json" target="_blank">OpenAPI Spec</a>
    <a href="/health" target="_blank">System Health</a>
  </div>
</header>

<div class="container">
  <div class="grid">
    <!-- Left Column: Webhook Simulator -->
    <div class="card">
      <div class="card-title">
        <span>GitHub PR Webhook Trigger</span>
        <span class="tag">Test Case 1</span>
      </div>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 14px;">
        Simulate incoming Pull Request event to run sandbox linters and halt at HITL approval gate.
      </p>

      <div class="form-group">
        <label>Repository URL</label>
        <input type="text" id="repoUrl" value="https://github.com/octocat/Hello-World">
      </div>
      <div class="form-group">
        <label>Branch Name</label>
        <input type="text" id="branchName" value="feature/refactor-pricing">
      </div>
      <div class="form-group">
        <label>Pull Request URL</label>
        <input type="text" id="prUrl" value="https://github.com/octocat/Hello-World/pull/42">
      </div>
      <div class="form-group">
        <label>Candidate Code (with PEP 8 issues)</label>
        <textarea id="codeContents" rows="7">def calculate_total_price(items, tax_rate):
    # Calculate totals with loops
    total = 0
    for item in items:
      total = total + item['price']
    tax=total*tax_rate
    return total+tax
</textarea>
      </div>

      <button class="btn btn-primary" id="btnIngest" onclick="triggerWebhook()">
        <span id="btnIngestText">Trigger Code Review Pipeline</span>
        <div class="loader" id="ingestLoader"></div>
      </button>
    </div>

    <!-- Right Column: Interactive HITL Session -->
    <div class="card" id="sessionCard">
      <div class="card-title">
        <span>Active Review Session (HITL Gate)</span>
        <span id="sessionStatus" class="status-badge status-paused">Awaiting Webhook</span>
      </div>

      <div id="noSessionNotice" style="padding: 40px 20px; text-align: center; color: var(--text-muted);">
        Click <strong>"Trigger Code Review Pipeline"</strong> to execute <code>fetch_pr_node</code>, <code>lint_code_node</code>, and <code>propose_refactor_node</code>.
      </div>

      <div id="sessionContent" style="display: none;">
        <div style="display: flex; gap: 24px; font-size: 13px; margin-bottom: 12px; flex-wrap: wrap;">
          <div><strong style="color: var(--text-muted);">Thread ID:</strong> <code id="lblThreadId" style="color: var(--accent);"></code></div>
          <div><strong style="color: var(--text-muted);">Next Node:</strong> <code id="lblNextNode" style="color: var(--accent-amber);">apply_changes_node</code></div>
          <div><strong style="color: var(--text-muted);">Branch:</strong> <span id="lblBranch"></span></div>
        </div>

        <div class="diff-container">
          <div>
            <label>Original PR Code</label>
            <div class="code-box" id="viewOriginalCode"></div>
          </div>
          <div>
            <label>Proposed Refactored Code (Clean Logic)</label>
            <div class="code-box" id="viewRefactoredCode"></div>
          </div>
        </div>

        <div style="margin-top: 14px;">
          <label>Sandbox Linter Diagnostics (Flake8 & Black)</label>
          <div class="code-box" id="viewLintErrors" style="max-height: 120px; color: #ff7b72;"></div>
        </div>

        <!-- Human in the loop Actions -->
        <div class="feedback-panel">
          <div class="card-title" style="margin-bottom: 8px;">
            <span>Human-in-the-Loop Validation Gate</span>
            <span class="tag">interrupt_before=["apply_changes_node"]</span>
          </div>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">
            Inspect proposed changes above. You can provide feedback to re-route and regenerate the proposal, or approve to commit back to GitHub.
          </p>

          <div class="form-group">
            <label>Reviewer Feedback (For Re-routing)</label>
            <input type="text" id="reviewerFeedback" value="Use list comprehensions instead of loops">
          </div>

          <div style="display: flex; gap: 12px;">
            <button class="btn btn-danger" style="flex: 1;" onclick="submitDecision(false)">
              <span>Reject & Re-route (Test Case 2)</span>
            </button>
            <button class="btn btn-success" style="flex: 1;" onclick="submitDecision(true)">
              <span>Approve & Commit (Test Case 3)</span>
            </button>
          </div>
        </div>

        <!-- Audit History -->
        <div style="margin-top: 16px;">
          <label>Audit History & Checkpoint Timeline</label>
          <div class="history-list" id="historyList"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  let currentThreadId = null;

  async function triggerWebhook() {
    const btn = document.getElementById("btnIngest");
    const loader = document.getElementById("ingestLoader");
    const btnText = document.getElementById("btnIngestText");

    btn.disabled = true;
    loader.style.display = "inline-block";
    btnText.textContent = "Running Pipeline...";

    const payload = {
      repository_url: document.getElementById("repoUrl").value,
      branch: document.getElementById("branchName").value,
      pr_url: document.getElementById("prUrl").value,
      code_contents: document.getElementById("codeContents").value
    };

    try {
      const res = await fetch("/api/webhooks/github", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        currentThreadId = data.thread_id;
        renderSession(data);
      } else {
        alert("Webhook Error: " + (data.detail || JSON.stringify(data)));
      }
    } catch (e) {
      alert("Network Error: " + e.message);
    } finally {
      btn.disabled = false;
      loader.style.display = "none";
      btnText.textContent = "Trigger Code Review Pipeline";
    }
  }

  async function submitDecision(approved) {
    if (!currentThreadId) {
      alert("No active review thread.");
      return;
    }

    const feedback = document.getElementById("reviewerFeedback").value;
    const payload = {
      approved: approved,
      feedback: feedback
    };

    try {
      const res = await fetch(`/api/reviews/${currentThreadId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        await refreshSessionState();
      } else {
        alert("Error: " + (data.detail || JSON.stringify(data)));
      }
    } catch (e) {
      alert("Network Error: " + e.message);
    }
  }

  async function refreshSessionState() {
    if (!currentThreadId) return;
    const res = await fetch(`/api/reviews/${currentThreadId}`);
    if (res.ok) {
      const data = await res.json();
      renderSession(data);
    }
  }

  function renderSession(data) {
    document.getElementById("noSessionNotice").style.display = "none";
    document.getElementById("sessionContent").style.display = "block";

    document.getElementById("lblThreadId").textContent = data.thread_id;
    document.getElementById("lblBranch").textContent = data.branch_name || "main";

    const statusBadge = document.getElementById("sessionStatus");
    if (data.status === "changes_committed" || data.status === "completed") {
      statusBadge.textContent = "Committed (Completed)";
      statusBadge.className = "status-badge status-committed";
      document.getElementById("lblNextNode").textContent = "Completed (END)";
    } else {
      statusBadge.textContent = "Paused at Approval Checkpoint";
      statusBadge.className = "status-badge status-paused";
      document.getElementById("lblNextNode").textContent = (data.next_nodes && data.next_nodes[0]) || "apply_changes_node";
    }

    document.getElementById("viewOriginalCode").textContent = data.code_contents || document.getElementById("codeContents").value;
    document.getElementById("viewRefactoredCode").textContent = data.refactored_code || "# No refactored code yet";
    document.getElementById("viewLintErrors").textContent = data.lint_errors || "No lint errors.";

    // Render audit history
    const historyList = document.getElementById("historyList");
    historyList.innerHTML = "";
    if (data.history && data.history.length > 0) {
      data.history.forEach(item => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.innerHTML = `<span><strong>${item.node}</strong>: ${item.action || item.message || ''}</span> <span>${item.timestamp ? item.timestamp.split('T')[1].slice(0,8) : ''}</span>`;
        historyList.appendChild(div);
      });
    }
  }
</script>

</body>
</html>
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown events."""
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.version} on port {settings.port} [{settings.environment}]")
    yield
    logger.info(f"Shutting down {settings.app_name}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title="RookieStuff - Autonomous Code Review & Refactoring Agent",
        description=(
            "An autonomous, stateful code review and refactoring agent built with LangGraph, "
            "FastAPI, and GitHub API integration. Features isolated sandbox linting, "
            "persistent memory checkpoints, and Human-in-the-Loop (HITL) review gates."
        ),
        version=settings.version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(api_router)

    @app.get("/", tags=["Dashboard & Health"])
    async def index(request: Request):
        """
        Serves the interactive Human-in-the-Loop Review Dashboard for browser users,
        and JSON metadata for API clients.
        """
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            return HTMLResponse(content=DASHBOARD_HTML, status_code=200)

        return {
            "name": settings.app_name,
            "version": settings.version,
            "status": "online",
            "port": settings.port,
            "documentation": "/docs",
            "openapi": "/openapi.json",
            "dashboard": "/dashboard",
            "endpoints": {
                "webhook": "POST /api/webhooks/github",
                "approve": "POST /api/reviews/{thread_id}/approve",
                "review_state": "GET /api/reviews/{thread_id}",
            },
        }

    @app.get("/dashboard", tags=["Dashboard & Health"], response_class=HTMLResponse)
    async def dashboard():
        """Direct endpoint for interactive Human-in-the-Loop Review Dashboard."""
        return HTMLResponse(content=DASHBOARD_HTML, status_code=200)

    @app.get("/health", tags=["Dashboard & Health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "app": settings.app_name,
            "port": settings.port,
            "checkpointer": settings.checkpointer_type,
            "environment": settings.environment,
        }

    return app


app = create_app()
