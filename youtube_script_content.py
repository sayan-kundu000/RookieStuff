"""
Complete 45-Minute YouTube Video Script for RookieStuff.
Contains 15 structured scenes with exact timecodes, on-screen actions,
presenter cues, full spoken dialogue in simple, conversational language,
and technical pro-tips.
"""

SCENES = [
    # ====================================================
    # SCENE 1
    # ====================================================
    {
        "scene_num": 1,
        "timecode": "00:00 - 03:00",
        "title": "The Hook: 47 Comments on a Single Pull Request",
        "action": "[CAMERA: Close-up on Host at desk. Quick jump cuts. Behind host, a giant monitor displays a messy GitHub Pull Request covered in red linting complaints and angry reviewer comments.]",
        "dialogue": [
            "Look at this screen right here. Forty-seven comments on a single pull request. And what are they arguing about? Did someone find a multi-million-dollar security vulnerability? No! They are arguing about whether there should be two blank lines before a function, why an indentation is three spaces instead of four, and why someone wrote a four-line for-loop instead of a clean list comprehension.",
            "If you have ever worked as a professional software engineer, you know this pain deep in your soul. Senior developers spend half their working day acting like human spellcheckers, while junior developers wait three days just to get their code reviewed, only to get slammed with a dozen tiny nitpicks. It destroys developer morale, it bottlenecks release cycles, and frankly, it is a massive waste of human brainpower.",
            "What if you had a tireless, ultra-smart junior engineer sitting right next to your repository? The exact second someone opens a Pull Request on GitHub, this automated teammate steps in. It pulls the code, spins up an isolated security sandbox, runs strict syntax and formatting checks, fixes all the PEP 8 violations, refactors the code into idiomatic Python, and presents a beautiful, ready-to-merge proposal to the human team.",
            "And here is the critical part: it will NEVER blindly push changes to your production branch without your permission. It pauses at an electronic gate, summons a human engineer, listens to your review notes, regenerates the code if you want revisions, and only commits when you click the approve button.",
            "Welcome to RookieStuff. Today, we are going to build this autonomous code review and refactoring agent from absolute scratch. We will cover LangGraph state machines, FastAPI webhooks, subprocess sandboxes, Flake8, Black, Docker, and full Human-in-the-Loop persistent checkpoints. By the end of this video, you will know exactly how to build enterprise-grade AI agents that real companies can actually trust. Grab your coffee, smash that subscribe button, and let's dive in!"
        ],
        "presenter_tip": "Keep your energy high and expressive during the first 60 seconds! Show genuine frustration with nitpicky code reviews—every developer in your audience will immediately relate."
    },

    # ====================================================
    # SCENE 2
    # ====================================================
    {
        "scene_num": 2,
        "timecode": "03:00 - 06:30",
        "title": "The Problem: Why Traditional CI/CD and Simple AI Scripts Fail",
        "action": "[CAMERA: Split-screen. Host on the left; on the right, an animated diagram contrasts a passive red 'CI FAILED' box with an active AI Agent.]",
        "dialogue": [
            "Before we look at the code, let's understand why existing tools fail to solve this problem. Most teams already use a CI/CD pipeline—something like GitHub Actions, GitLab CI, or Jenkins. A developer pushes code, the CI runner spins up, runs a linter, and if there is a formatting error, it gives you a big red cross. 'CI Failed.'",
            "Why is that so frustrating? Because a red cross is passive and unhelpful. It tells you that you broke a rule, but it does not fix it for you. It puts the burden right back on the developer: 'Go figure it out, reformat your code, commit again, and wait another ten minutes for the pipeline to finish.' It creates friction without offering a solution.",
            "So developers thought: 'Hey, why don't we just pipe our code into an LLM like GPT-4?' But if you have ever tried doing that with a simple script, you ran into three massive brick walls. First, basic scripts are stateless. You send code to an API, get a response, and the connection closes. If a reviewer says, 'I don't like this approach, try again,' the script has no memory of what it did two seconds ago.",
            "Second, basic LLM scripts are prone to hallucination. A naive language model might decide to rewrite your entire function, change parameter names that other files depend on, or accidentally drop critical business logic. You cannot let an unconstrained model touch company code without automated verification.",
            "And third—the biggest fear of every engineering director—is unauthorized write access. If an automated AI script has write permissions to your Git repo, one bad hallucination could overwrite the main branch, break production, and take down the entire company website on a Friday afternoon! We need a system that has intelligence, memory, strict boundaries, and an unshakeable human gate. That is the architecture of RookieStuff."
        ],
        "presenter_tip": "Use your hands to illustrate the difference between a linear chain (straight line, no memory) and a stateful graph (looping, remembering, pausing)."
    },

    # ====================================================
    # SCENE 3
    # ====================================================
    {
        "scene_num": 3,
        "timecode": "06:30 - 10:00",
        "title": "The Tech Stack: LangGraph, FastAPI, Docker, and Sandbox Linters",
        "action": "[SCREEN SHARE: Full desktop view showing VS Code with the RookieStuff project folder open, highlighting requirements.txt and pyproject.toml.]",
        "dialogue": [
            "Let's look at the tech stack we chose for RookieStuff. Every single tool here was picked for a specific, battle-tested reason. We did not use bloated, experimental frameworks that break every Tuesday. We picked rock-solid tools.",
            "Pillar Number One: Python 3.11. Python is the native language of artificial intelligence and data science, and version 3.11 brings significant speed improvements and crisp error messages that make our static analysis fast and reliable.",
            "Pillar Number Two: LangGraph. Notice I did not say standard LangChain. We are using LangGraph. LangGraph allows us to build multi-actor, stateful applications as directed state machines. It gives us nodes for our actions, edges for our decisions, and persistent checkpointers so our agent can pause, sleep for three hours while a human eats lunch, and wake up right where it left off.",
            "Pillar Number Three: FastAPI and Uvicorn. When GitHub fires a webhook event, we need a web server that responds in milliseconds. FastAPI is natively asynchronous, extremely fast, and automatically creates interactive Swagger documentation without us writing a single line of frontend code.",
            "Pillar Number Four: Isolated Subprocess Linters. We use Python's built-in `ast` module for instant syntax validation, paired with Flake8 and Black. We run these inside temporary quarantined folders using subprocesses so that untrusted code from pull requests can never harm our host machine.",
            "And Pillar Number Five: Docker and Pytest. We have a complete 16-test automated verification suite that runs in under 42 seconds, and everything is packaged into a production-ready Docker container so you can deploy it to any cloud with a single command."
        ],
        "presenter_tip": "Scroll slowly through requirements.txt so viewers can see the clean dependencies: langgraph, langchain-openai, fastapi, uvicorn, flake8, black, pydantic-settings."
    },

    # ====================================================
    # SCENE 4
    # ====================================================
    {
        "scene_num": 4,
        "timecode": "10:00 - 13:00",
        "title": "Starting the Engine: Live Server Boot on Port 3000",
        "action": "[SCREEN SHARE: Open terminal. Type command `uvicorn main:app --port 3000`. Show instant startup logs. Open Chrome to http://localhost:3000.]",
        "dialogue": [
            "Alright, enough theory—let's see this thing run! I'm opening my terminal inside the project directory, activating our virtual environment, and running the server command: `uvicorn main:app --port 3000`.",
            "Look at that terminal output. In less than one second, our lifespan manager boots up, configures our persistent memory checkpointer, mounts our API routes, and binds to port 3000. Now let's open Google Chrome and navigate to `http://localhost:3000`.",
            "Boom! Look at what we built. We have a custom, high-tech dark-mode dashboard running right out of the box. On the top navigation, you have instant links to the Swagger API docs at `/docs`, ReDoc at `/redoc`, the raw OpenAPI spec, and our live health check endpoint.",
            "The dashboard itself is split into two clean operational zones. On the left is our **GitHub PR Webhook Trigger**, which lets us simulate incoming pull request events with custom repository URLs, branches, and sample code. On the right is the **Active Review Session**, where the human engineer inspects the agent's work, reviews diagnostics, and controls the Human-in-the-Loop gate. Let's run our first test case live!"
        ],
        "presenter_tip": "Showcase how clean the dashboard looks! Emphasize that it is served natively by FastAPI with zero React or Node.js dependencies required."
    },

    # ====================================================
    # SCENE 5
    # ====================================================
    {
        "scene_num": 5,
        "timecode": "13:00 - 15:30",
        "title": "Live Demo Part 1: Webhook Ingestion & The HITL Pause Gate",
        "action": "[SCREEN SHARE: Zoom into the left-hand panel of the dashboard. Inspect the pre-filled candidate code with PEP 8 errors. Click the green 'Trigger Code Review Pipeline' button.]",
        "dialogue": [
            "Let's look at the candidate code in our trigger panel. Notice the deliberate rookie mistakes: `total = 0`, an unformatted loop with two-space indentation, no spaces around the multiplication operator `tax=total*tax_rate`, and missing blank lines. This is classic messy code that wastes reviewer time.",
            "Now watch what happens when I click this green button: 'Trigger Code Review Pipeline'. The button enters a loading state. Behind the scenes, FastAPI receives our webhook, generates a unique thread ID, and launches LangGraph.",
            "LangGraph executes `fetch_pr_node`, routes into `lint_code_node` where Flake8 and Black inspect the code in our sandbox, and then invokes `propose_refactor_node` to draft an improved version. And look at the right-hand panel now!",
            "It just updated in real time! Look at the top status badge: it is glowing yellow, displaying **Paused at Approval Checkpoint**. Look at `Next Node`: it says `apply_changes_node`. The agent finished its analysis, generated the refactored code on the right side, but because of our `interrupt_before` setting, it slammed on the brakes. It refused to write to GitHub. It is patiently waiting for us."
        ],
        "presenter_tip": "Point your mouse to the side-by-side diff view. Highlight the original code vs. the clean refactored code and show the Flake8 diagnostic box directly beneath it."
    },

    # ====================================================
    # SCENE 6
    # ====================================================
    {
        "scene_num": 6,
        "timecode": "15:30 - 18:00",
        "title": "Live Demo Part 2: Reviewer Feedback, Re-routing, and Approval",
        "action": "[SCREEN SHARE: Scroll down to the Human-in-the-Loop panel. Type 'Use list comprehensions instead of loops' in the feedback field. Click 'Reject & Re-route'. Watch code update. Then click 'Approve & Commit'.]",
        "dialogue": [
            "Now let's test what happens when the human reviewer is not satisfied. Let's say I am a senior engineer reviewing this PR. The refactored code is clean, but I notice it is still using an accumulator loop. I want modern, pythonic code.",
            "I go to the feedback box right here, and I type: `Use list comprehensions instead of loops`. Now I click the red button: **Reject & Re-route (Test Case 2)**.",
            "Watch the screen! The agent immediately accepts the rejection, writes my feedback into the checkpointer state, rewinds execution back to `propose_refactor_node`, and regenerates the draft! Look at the code box now: `item_prices = [item['price'] for item in items]` and `subtotal = sum(item_prices)`! It dynamically rewrote the implementation specifically following my instructions!",
            "And notice where it stopped: it is paused right back at the approval gate! It did not commit yet. Now that I am completely happy, I click the green button: **Approve & Commit (Test Case 3)**.",
            "Boom! The status badge instantly turns bright green: **Committed (Completed)**! The gate unlocked, `apply_changes_node` executed, the commit was pushed to the branch, and right here in the audit timeline, you can see the exact Git Commit SHA hash returned by the API. That is full-lifecycle autonomous review with zero safety compromises!"
        ],
        "presenter_tip": "Celebrate the green badge! Emphasize how magical it feels to see an AI agent rewrite code according to human feedback without losing its place in the pipeline."
    },

    # ====================================================
    # SCENE 7
    # ====================================================
    {
        "scene_num": 7,
        "timecode": "18:00 - 21:30",
        "title": "Under the Hood: Why LangGraph? State Machines vs. Chains",
        "action": "[SCREEN SHARE: Switch to VS Code. Open `app/graph/workflow.py`. Highlight the `StateGraph` builder and edge declarations.]",
        "dialogue": [
            "Now that you've seen the live magic, let's open the hood and see how the engine is built. We are in `app/graph/workflow.py`. This is where the LangGraph state machine is defined.",
            "Why did we use LangGraph instead of a simple script or a chain? Because in traditional AI chains, everything must flow in a straight line: A leads to B, B leads to C, and then it terminates. But software engineering is inherently cyclical! You write code, you test it, you get feedback, you go backward, you fix it, and you test it again.",
            "Look at lines 45 through 55 in `workflow.py`. We initialize `StateGraph(ReviewState)`. We add our four core nodes: `fetch_pr_node`, `lint_code_node`, `propose_refactor_node`, and `apply_changes_node`.",
            "Then we add our sequential edges: `START` connects to `fetch_pr_node`, which connects to `lint_code_node`, which connects to `propose_refactor_node`, which connects to `apply_changes_node`, which connects to `END`.",
            "Now look at line 62: `graph = builder.compile(checkpointer=checkpointer, interrupt_before=interrupt_before)`. That single line of code is where the entire magic happens. By passing `interrupt_before=['apply_changes_node']`, LangGraph automatically injects an execution boundary before the write node. It gives us pause-and-resume capability for free!"
        ],
        "presenter_tip": "Use your cursor to highlight `builder.add_node` and `builder.add_edge`. Explain that nodes are verbs (actions) and edges are the roads between them."
    },

    # ====================================================
    # SCENE 8
    # ====================================================
    {
        "scene_num": 8,
        "timecode": "21:30 - 24:30",
        "title": "The State Schema: Anatomy of the ReviewState Dictionary",
        "action": "[SCREEN SHARE: In VS Code, open `app/state.py`. Highlight the `ReviewState(TypedDict)` definition.]",
        "dialogue": [
            "Now let's look at `app/state.py`. In LangGraph, data does not float around in random global variables. All data is stored in a centralized, strongly typed dictionary called the State Schema. Here is our `ReviewState` class.",
            "Let's walk through the required keys. First, `pr_url: str`. This is the web address of the target pull request on GitHub, anchoring the entire session. Second, `code_contents: str`. This holds the original, unmodified code from the PR.",
            "Third, `lint_errors: str`. When our sandbox linter runs, all Flake8 and Black diagnostic messages are captured and stored here. Fourth, `refactored_code: str`. This stores the proposed clean Python code drafted by our refactoring engine.",
            "Fifth and sixth, `is_approved: bool` and `reviewer_feedback: Optional[str]`. These two keys manage human governance. `is_approved` tells the graph whether the human clicked approve, and `reviewer_feedback` captures any revision requests.",
            "And seventh, look at `history: List[Dict[str, Any]]`. This is an append-only audit ledger. Every time a node executes, our `add_history_entry` helper appends a timestamped record capturing the node name, the action taken, and detailed metadata. Nothing is ever lost or hidden."
        ],
        "presenter_tip": "Highlight the elegance of TypedDict. It gives developers full autocomplete and type safety in Python while serializing cleanly to JSON."
    },

    # ====================================================
    # SCENE 9
    # ====================================================
    {
        "scene_num": 9,
        "timecode": "24:30 - 28:00",
        "title": "The Execution Sandbox: AST Checks, Flake8, and Black",
        "action": "[SCREEN SHARE: In VS Code, open `app/tools/sandbox.py`. Walk through `check_syntax` and `@tool run_linter_tool`.]",
        "dialogue": [
            "Now let's examine one of the coolest parts of this project: the security sandbox in `app/tools/sandbox.py`. When you are building an automated system that handles untrusted code from the internet, you can never just run that code inside your main server process.",
            "Look at line 14: `check_syntax()`. Before we even touch the disk, we pass the code into Python's built-in `ast.parse()`. If someone submitted code with an unclosed parenthesis or a malformed statement, the AST parser catches it in microseconds! It extracts the exact line number, column offset, and error message, failing fast without wasting CPU cycles.",
            "If the syntax is valid, we enter `run_linter_tool`. Notice the `@tool` decorator on line 28. This turns our Python function into an official LangChain tool with full docstrings and metadata.",
            "Inside the tool, look at line 35: `with tempfile.TemporaryDirectory(prefix='rookiestuff_sandbox_') as tmp_dir:`. We create an isolated, unique temporary folder on disk. We write the candidate code into `candidate_code.py`. Then we launch two external subprocesses: Flake8 with `--max-line-length=100`, and Black with `--check --diff`.",
            "We enforce a strict 15-second timeout on both subprocesses so no runaway code can ever hang the server. If errors are found, we clean up the file paths so the error messages look clean. And the moment the `with` block exits, Python automatically deletes the entire temporary folder from the file system. Zero disk residue, zero cross-contamination!"
        ],
        "presenter_tip": "Emphasize how professional this is. Running untrusted code in a temporary directory with a timeout is exactly how enterprise cloud runners work."
    },

    # ====================================================
    # SCENE 10
    # ====================================================
    {
        "scene_num": 10,
        "timecode": "28:00 - 31:30",
        "title": "The AI Brain: propose_refactor_node and Prompt Engineering",
        "action": "[SCREEN SHARE: In VS Code, open `app/graph/nodes.py`. Highlight the prompt construction inside `propose_refactor_node`.]",
        "dialogue": [
            "Now let's look at how the agent actually writes code. In `app/graph/nodes.py`, we have `propose_refactor_node`. This is where the language model comes to work.",
            "Look at how we initialize `ChatOpenAI`: we pass `model='gpt-4o-mini'` and set `temperature=0.0`. In code refactoring, you do not want wild creativity; you want deterministic precision and strict adherence to programming logic.",
            "Now look at our prompt design. We don't just say 'Fix this code.' We provide three distinct sections: `### Original Code`, `### Current Code`, and `### Linting & Formatting Errors`. This gives the model the exact coordinates of what went wrong.",
            "Look at line 155: if `reviewer_feedback` is present in the state, we inject an alert banner into the prompt: `### CRITICAL Reviewer Feedback (MUST ADDRESS)`. This tells the model: 'Pay attention! The human engineer specifically asked for list comprehensions, so prioritize that above all else.'",
            "And look at line 20: our `clean_code_block` helper. When LLMs write code, they almost always wrap it in markdown backticks: ````python ... ````. If you try to compile code with backticks, Python crashes. Our regex helper strips away the fences, leaving pure, executable Python. And if you are running offline without an API key, our deterministic fallback engine handles the refactoring automatically!"
        ],
        "presenter_tip": "Show viewers the `clean_code_block` function. Many junior developers struggle with LLMs returning markdown fences, so this is a great practical tip."
    },

    # ====================================================
    # SCENE 11
    # ====================================================
    {
        "scene_num": 11,
        "timecode": "31:30 - 34:30",
        "title": "The Re-route Magic: How as_node Rewinds the State Machine",
        "action": "[SCREEN SHARE: In VS Code, open `app/graph/workflow.py`. Highlight the `rollback_and_reroute_with_feedback` function.]",
        "dialogue": [
            "Now I want to show you one of the most powerful tricks in LangGraph that separates beginner scripts from expert architectures: how to rewind a thread when a human rejects a draft.",
            "Look at `rollback_and_reroute_with_feedback()` in `workflow.py`. When a reviewer clicks reject, the graph is currently halted in front of `apply_changes_node`. How do we tell LangGraph to step backward to `propose_refactor_node`?",
            "Look at line 102: `graph.update_state(config, {'is_approved': False, 'reviewer_feedback': feedback}, as_node='lint_code_node')`. That parameter right there—`as_node='lint_code_node'`—is the golden key!",
            "In LangGraph, when you update the state and declare that the update came from `lint_code_node`, LangGraph looks at its edge table. It asks: 'What node comes after `lint_code_node`?' And the answer is: `propose_refactor_node`!",
            "So LangGraph automatically moves its execution pointer back to `propose_refactor_node`. When we call `graph.invoke(None, config)`, the agent executes the refactoring node again, applies the human's feedback, moves toward the write gate, and pauses once more! We achieved a clean, stateful feedback loop in less than ten lines of code."
        ],
        "presenter_tip": "Slow down your speech here and emphasize `as_node`. This is an advanced LangGraph concept that interviewers and senior engineers love to see."
    },

    # ====================================================
    # SCENE 12
    # ====================================================
    {
        "scene_num": 12,
        "timecode": "34:30 - 37:30",
        "title": "The Web Server: FastAPI Endpoints, Webhooks, and OpenAPI",
        "action": "[SCREEN SHARE: Open `app/api/routes.py` in VS Code. Walk through the webhook and approval routes. Then switch to browser and show `/docs` Swagger UI.]",
        "dialogue": [
            "Now let's talk about the web layer. How does GitHub talk to our agent, and how do human reviewers talk to our agent? We open `app/api/routes.py`.",
            "Our first major endpoint is `POST /api/webhooks/github`. It accepts incoming payloads. Notice that our schema supports both full GitHub webhook events and simplified test payloads. It extracts the PR URL, generates a unique thread ID using `uuid4()`, initializes the review state, invokes the graph up to the interrupt checkpoint, and returns an HTTP 201 response.",
            "Our second endpoint is `POST /api/reviews/{thread_id}/approve`. It accepts an approval payload with `approved: bool` and `feedback: str`. If approved is False, it calls our rollback helper. If approved is True, it calls `approve_and_apply`, committing the code to GitHub and returning the commit SHA.",
            "Now let's flip over to the browser and look at `http://localhost:3000/docs`. Because we built this with FastAPI, we get this interactive Swagger UI for free! You can click on any endpoint, hit 'Try it out', execute live requests, inspect response schemas, and download the full OpenAPI 3.1 JSON specification. It makes testing and API integration an absolute joy."
        ],
        "presenter_tip": "Click 'Try it out' on the `/health` endpoint in Swagger UI and execute it live on screen to show how fast FastAPI responds."
    },

    # ====================================================
    # SCENE 13
    # ====================================================
    {
        "scene_num": 13,
        "timecode": "37:30 - 41:00",
        "title": "Testing and DevOps: 16 Pytest Checks & Docker Containerization",
        "action": "[SCREEN SHARE: Open terminal. Run command `pytest -v`. Watch all 16 tests pass green. Then open `Dockerfile` and `docker-compose.yml` in VS Code.]",
        "dialogue": [
            "No software project is complete without rigorous automated testing. In our `tests/` directory, we wrote 16 automated tests covering every aspect of the system. Let's run `pytest -v` in the terminal right now.",
            "Look at those green dots flying by! In `test_sandbox_tool.py`, we test that broken syntax is caught instantly, that Flake8 errors are identified, and that clean code passes. In `test_graph_routing.py`, we test that the graph halts at the gate, that review rejections re-route properly, and that approval commits cleanly.",
            "And in `test_api_endpoints.py`, we test all three required evaluation workflows: Webhook Ingestion, Reviewer Re-route, and Git Commit Write Back. All 16 tests pass with 100% success!",
            "Now let's look at deployment. In `Dockerfile`, we use a lightweight `python:3.11-slim` base image, install git and curl, install our requirements with layer caching, expose port 3000, and configure an automated health check probe that pings `/health` every 30 seconds.",
            "And with our `docker-compose.yml`, you can type `docker-compose up --build` and have the entire system running inside an isolated production container in seconds. It is completely portable and cloud-ready."
        ],
        "presenter_tip": "Let the pytest output finish on screen before speaking about Docker. A screen full of passing green tests is visual proof of quality."
    },

    # ====================================================
    # SCENE 14
    # ====================================================
    {
        "scene_num": 14,
        "timecode": "41:00 - 43:00",
        "title": "How to Run This Right Now: Cloning the GitHub Repository",
        "action": "[SCREEN SHARE: Open Chrome to `https://github.com/sayan-kundu000/RookieStuff`. Show the clean repo, commit history, and README.]",
        "dialogue": [
            "If you want to run RookieStuff on your own computer right now, it takes less than two minutes. The entire repository is published and open on GitHub at `https://github.com/sayan-kundu000/RookieStuff`.",
            "All you have to do is clone the repo: `git clone https://github.com/sayan-kundu000/RookieStuff.git`. Navigate into the folder and copy the environment template: `cp .env.example .env`.",
            "Install the dependencies with `pip install -r requirements.txt`. Run the tests with `pytest`. And then launch the server with `uvicorn main:app --port 3000`.",
            "Open your browser to `http://localhost:3000`, and you have the full interactive dashboard running locally on your machine. You can even run it with zero API keys because our built-in mock fallbacks let you test and demonstrate every single feature offline!"
        ],
        "presenter_tip": "Put the GitHub URL in a bold graphic on screen so viewers can easily pause and type it into their browser."
    },

    # ====================================================
    # SCENE 15
    # ====================================================
    {
        "scene_num": 15,
        "timecode": "43:00 - 45:00",
        "title": "Conclusion: The Future of Autonomous Engineering & Outro",
        "action": "[CAMERA: Host back on full screen. Warm studio lighting. Outro music fades in softly. GitHub star reminder and video cards appear on screen.]",
        "dialogue": [
            "We have covered a massive amount of ground today. We took a real-world software engineering problem—the painful bottleneck of manual code reviews—and solved it using modern, stateful AI agent architecture.",
            "We didn't just build a simple chatbot that spews text. We built a disciplined, stateful machine with LangGraph. We quarantined untrusted code in a subprocess sandbox. We enforced PEP 8 standards with Flake8 and Black. We built an asynchronous web API with FastAPI. And most importantly, we put human engineers in control with persistent checkpointer interrupt gates.",
            "This is the future of software engineering. AI is not going to replace developers; but developers who understand how to build and collaborate with autonomous AI agents are going to replace developers who don't.",
            "If you found this video valuable, please hit that like button, subscribe to the channel, and share this with your engineering teammates. Drop a comment below letting me know what agentic workflow you want us to build next. The full code and 37-page documentation PDF are linked in the description below. Thank you for watching, keep building great software, and I will see you in the next one!"
        ],
        "presenter_tip": "End with a confident, warm smile. Point to the screen where the subscribe button and GitHub link will appear."
    }
]

