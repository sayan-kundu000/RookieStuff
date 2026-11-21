import pytest
from app.tools.sandbox import run_linter_tool, check_syntax


def test_syntax_checker_identifies_syntax_errors():
    """Assert syntax checker immediately catches malformed Python code."""
    broken_code = "def invalid_syntax(x\n    return x + 1"
    is_valid, err_msg = check_syntax(broken_code)
    assert not is_valid
    assert "SyntaxError" in err_msg


def test_linter_tool_identifies_syntax_errors():
    """Lint Tool Isolation: Assert the linter tool successfully identifies syntax errors in a bad code string."""
    bad_code = "def calculate(val):\n    if val >\n        return True"
    result = run_linter_tool.invoke({"code_string": bad_code})
    assert "SYNTAX ERROR DETECTED" in result
    assert "SyntaxError" in result


def test_linter_tool_identifies_flake8_and_black_errors():
    """Assert the sandbox identifies PEP 8 violations and formatting issues."""
    unformatted_code = (
        "def compute(a,b):\n"
        "  result=a*b+2\n"
        "  return result\n"
        "x=compute(1,2)\n"
    )
    result = run_linter_tool.invoke({"code_string": unformatted_code})
    assert "Flake8 Lint Errors" in result or "Black Formatting Issues" in result
    assert "E111" in result or "E225" in result or "reformatted" in result


def test_linter_tool_passes_clean_code():
    """Assert perfectly formatted, PEP 8 compliant code passes without errors."""
    clean_code = (
        "def compute_area(width: float, height: float) -> float:\n"
        '    """Calculate the area of a rectangle."""\n'
        "    return width * height\n"
        "\n"
        "\n"
        "TOTAL_AREA = compute_area(10.0, 5.0)\n"
    )
    result = run_linter_tool.invoke({"code_string": clean_code})
    assert "SUCCESS" in result
    assert "clean" in result.lower()


def test_linter_tool_handles_empty_input():
    """Assert empty or whitespace code strings return appropriate error."""
    result = run_linter_tool.invoke({"code_string": "   \n\t  "})
    assert "ERROR" in result
    assert "Empty code" in result
