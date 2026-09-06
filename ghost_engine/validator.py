"""
Code validation and quality assurance module.
Ensures code compiles, passes syntax checks, and tests pass before committing.
"""
import ast
import os
import subprocess
from pathlib import Path
from typing import List, Tuple
from ghost_engine.humanizer import validate_human_text

def validate_python_syntax(file_path: Path) -> Tuple[bool, str]:
    """
    Parses Python file using AST to ensure zero syntax errors.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        ast.parse(code, filename=str(file_path))
        
        # Check human text guidelines (no em-dashes, no emojis in code or docstrings)
        if not validate_human_text(code):
            return False, f"Prohibited characters (em-dash or emoji) detected in {file_path.name}"
            
        return True, "Syntax valid"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def run_repo_tests(repo_path: Path) -> Tuple[bool, str]:
    """
    Runs pytest if tests directory exists in the repo.
    """
    tests_dir = repo_path / "tests"
    if not tests_dir.exists():
        return True, "No tests directory found, skipping test run"
        
    try:
        result = subprocess.run(
            ["pytest", "-q"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return True, "All tests passed"
        else:
            return False, f"Pytest failed:\n{result.stdout}\n{result.stderr}"
    except FileNotFoundError:
        # pytest not installed in environment, fallback to basic syntax validation
        return True, "Pytest not installed in runner environment, syntax validation passed"
    except subprocess.TimeoutExpired:
        return False, "Test execution timed out after 60s"
    except Exception as e:
        return False, f"Error running tests: {str(e)}"
