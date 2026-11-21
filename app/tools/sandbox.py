import ast
import os
import sys
import tempfile
import subprocess
from typing import Dict, Any, Tuple
from langchain_core.tools import tool


def check_syntax(code_string: str) -> Tuple[bool, str]:
    """
    Validate Python syntax using ast.parse before running linters.
    Returns (is_valid, error_message).
    """
    try:
        ast.parse(code_string)
        return True, ""
    except SyntaxError as exc:
        return False, f"SyntaxError at line {exc.lineno}, col {exc.offset}: {exc.msg}"
    except Exception as exc:
        return False, f"CompilationError: {str(exc)}"


@tool
def run_linter_tool(code_string: str) -> str:
    """Writes python code to a temporary file and runs flake8 analysis."""
    if not code_string or not code_string.strip():
        return "ERROR: Empty code provided. Nothing to lint."

    # 1. Early syntax check for quick error isolation
    syntax_ok, syntax_err = check_syntax(code_string)
    if not syntax_ok:
        return f"SYNTAX ERROR DETECTED:\n{syntax_err}"

    # 2. Isolated sandbox execution
    with tempfile.TemporaryDirectory(prefix="rookiestuff_sandbox_") as tmp_dir:
        temp_file = os.path.join(tmp_dir, "candidate_code.py")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(code_string)

            errors = []

            # Run flake8
            try:
                flake8_res = subprocess.run(
                    [sys.executable, "-m", "flake8", "--max-line-length=100", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if flake8_res.returncode != 0 and flake8_res.stdout.strip():
                    # Clean up temporary path from error messages for readability
                    clean_flake8 = flake8_res.stdout.replace(temp_file, "candidate_code.py")
                    errors.append(f"--- Flake8 Lint Errors ---\n{clean_flake8.strip()}")
            except subprocess.TimeoutExpired:
                errors.append("Flake8 check timed out after 15 seconds.")
            except Exception as e:
                errors.append(f"Flake8 execution failed: {str(e)}")

            # Run black --check
            try:
                black_res = subprocess.run(
                    [sys.executable, "-m", "black", "--check", "--line-length=100", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if black_res.returncode != 0:
                    err_msg = black_res.stderr.strip() or black_res.stdout.strip()
                    clean_black = err_msg.replace(temp_file, "candidate_code.py")
                    errors.append(f"--- Black Formatting Issues ---\n{clean_black}")
            except subprocess.TimeoutExpired:
                errors.append("Black format check timed out after 15 seconds.")
            except Exception as e:
                errors.append(f"Black execution failed: {str(e)}")

            if errors:
                return "\n\n".join(errors)
            return "SUCCESS: Code passed all linting and formatting checks (flake8 and black clean)."

        except Exception as exc:
            return f"SANDBOX ERROR: Failed to execute linter sandbox: {str(exc)}"
