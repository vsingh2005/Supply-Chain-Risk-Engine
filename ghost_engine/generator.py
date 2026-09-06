"""
Code Generator and Task Applier.
Applies roadmap actions or calls LLM for dynamic incremental improvements.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
from ghost_engine.humanizer import clean_commit_message
from ghost_engine.validator import validate_python_syntax

class CodeGenerator:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()

    def apply_task(self, task: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Applies a roadmap task's file operations to the repository.
        Returns (success, message, commit_msg).
        """
        task_id = task.get("id", "task")
        commit_msg = clean_commit_message(task.get("commit_message", f"feat: implement {task_id}"))
        files_changed: List[str] = []
        
        for change in task.get("changes", []):
            rel_path = change.get("path")
            content = change.get("content", "")
            action = change.get("action", "write")
            
            target_file = self.repo_path / rel_path
            
            if action == "delete":
                if target_file.exists():
                    target_file.unlink()
                    files_changed.append(f"Deleted {rel_path}")
            else:
                # write or create
                target_file.parent.mkdir(parents=True, exist_ok=True)
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content.strip() + "\n")
                
                # If Python file, validate syntax immediately
                if rel_path.endswith(".py"):
                    is_valid, err = validate_python_syntax(target_file)
                    if not is_valid:
                        return False, f"Failed syntax check on {rel_path}: {err}", commit_msg
                        
                files_changed.append(f"Updated {rel_path}")
                
        return True, f"Applied {len(files_changed)} file changes", commit_msg
