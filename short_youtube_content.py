"""
Streamlined, Concise YouTube Video Script for RookieStuff.
Target Runtime: ~10-12 Minutes.
Super simple language, crystal clear presenter action cues,
and concise explanations.
"""

SHORT_SCENES = [
    {
        "num": 1,
        "time": "00:00 - 02:00",
        "title": "The Hook: Why We Built RookieStuff",
        "action": "[ON CAMERA: Smile at camera. Show a messy GitHub Pull Request on screen with 20+ nitpicky comments about missing spaces and indentation.]",
        "speech": (
            "Hey everyone! Look at this pull request. Twenty comments arguing about missing spaces, "
            "wrong indentation, and messy loops. Senior developers spend hours every week pointing out "
            "these rookie mistakes, while junior developers wait days just to get their code approved.\n\n"
            "Today, we are fixing that with RookieStuff. It is an autonomous AI agent built with LangGraph, "
            "FastAPI, and Docker. The moment someone opens a Pull Request on GitHub, RookieStuff steps in. "
            "It runs code safety checks in a sandbox, fixes all formatting errors, writes clean Python code, "
            "and pauses at a human approval gate. It will never push code until you say yes. Let's see how it works!"
        ),
        "tip": "Keep your energy upbeat! Make the problem relatable in the first 30 seconds."
    },
    {
        "num": 2,
        "time": "02:00 - 04:00",
        "title": "What We Used: The Core Tech Stack",
        "action": "[SCREEN SHARE: Show VS Code with requirements.txt and the architecture diagram on screen.]",
        "speech": (
            "Let's quickly talk about what we used to build this. We chose five powerful tools:\n\n"
            "1. Python 3.11: The foundation. Fast, modern, and reliable.\n"
            "2. LangGraph: The brain. Unlike simple AI chatbots that forget everything, LangGraph is a state "
            "machine. It remembers every step, can loop backward if we reject a draft, and pauses whenever we want.\n"
            "3. Flake8 & Black: The quality inspectors. Flake8 checks PEP 8 style rules and bugs, while Black "
            "makes formatting clean and consistent.\n"
            "4. FastAPI: The web engine. It listens for GitHub webhooks and serves our web dashboard on port 3000.\n"
            "5. Docker & Pytest: Container portability and a rock-solid 16-test verification suite."
        ),
        "tip": "Explain LangGraph simply: it's not a straight line, it's a map with loops and pauses."
    },
    {
        "num": 3,
        "time": "04:00 - 06:30",
        "title": "Live Demo Part 1: Launching & Ingestion",
        "action": "[SCREEN SHARE: Open terminal. Run `.\\run.bat`. Open browser to `http://localhost:3000`. Click 'Trigger Code Review Pipeline'.]",
        "speech": (
            "Now let's see it in action! In our terminal, we just run `.\\run.bat` or use Uvicorn. "
            "In one second, our server boots up on port 3000. Let's open `http://localhost:3000` in Google Chrome.\n\n"
            "Here is our dashboard! On the left side, we have our GitHub PR simulator. Notice the sample code: "
            "it has bad two-space indentation, no spaces around operators, and an unformatted accumulator loop.\n\n"
            "Now I click 'Trigger Code Review Pipeline'. Behind the scenes, the agent fetches the code, "
            "runs Flake8 and Black inside an isolated temporary sandbox folder, and asks the LLM to refactor it. "
            "And look at the right side now: the status is glowing yellow: 'Paused at Approval Checkpoint'. "
            "The agent created clean code on the right, but it stopped right before writing to GitHub. It's waiting for us!"
        ),
        "tip": "Point your mouse to the side-by-side code boxes showing before and after."
    },
    {
        "num": 4,
        "time": "06:30 - 09:00",
        "title": "Live Demo Part 2: Feedback Re-route & One-Click Commit",
        "action": "[SCREEN SHARE: Type 'Use list comprehensions instead of loops' in feedback box. Click 'Reject & Re-route'. Watch code change. Click 'Approve & Commit'.]",
        "speech": (
            "Now here is the coolest feature: Human-in-the-Loop review feedback.\n\n"
            "Suppose I look at this proposal and say: 'The formatting is clean, but I want modern list comprehensions.' "
            "I type into the feedback box: 'Use list comprehensions instead of loops', and click the red button: 'Reject & Re-route'.\n\n"
            "Watch this! The agent rewinds its state back to the refactor node, reads my feedback, and rewrites the code! "
            "Look at the code box now: it changed to `item_prices = [item['price'] for item in items]` and `sum(item_prices)`. "
            "It listened to my exact instructions and paused right back at the gate.\n\n"
            "Now that I love the code, I click 'Approve & Commit'. Instantly, the status turns green: 'Committed (Completed)'! "
            "The agent authored a real Git commit on the branch, and returned the unique commit SHA hash right here in the audit log."
        ),
        "tip": "Show the commit SHA hash in the audit timeline. That proves the write succeeded."
    },
    {
        "num": 5,
        "time": "09:00 - 11:00",
        "title": "Under the Hood, Tests, and Wrap-Up",
        "action": "[SCREEN SHARE: Terminal running `pytest -v`. Show 16 passing tests. Then show GitHub repo page.]",
        "speech": (
            "Under the hood, this safety is powered by LangGraph's `interrupt_before=['apply_changes_node']`. "
            "When we reject, we update state with `as_node='lint_code_node'`, which rewinds the execution pointer.\n\n"
            "Let's run `pytest -v` in the terminal. All 16 automated tests pass in just a few seconds—verifying syntax checks, "
            "sandbox isolation, feedback re-routing, and GitHub commits.\n\n"
            "The entire project is open source and published on GitHub right now at `github.com/sayan-kundu000/RookieStuff`. "
            "You can clone it, run `.\\run.bat`, and test it locally with zero API keys required thanks to our built-in offline fallbacks.\n\n"
            "If this helped you understand how to build safe, stateful AI agents, smash the like button, subscribe, and star the repo. "
            "Thanks for watching, and happy coding!"
        ),
        "tip": "Smile, wave, and point to the description box where links are located."
    }
]
