"""
Task and Roadmap state manager for tracking repository progression.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

class TaskManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.ghost_dir = self.repo_path / ".ghost"
        self.state_file = self.ghost_dir / "state.json"
        self.roadmap_file = self.ghost_dir / "roadmap.json"
        
        self.ghost_dir.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self.roadmap = self._load_roadmap()

    def _load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "current_task_index": 0,
            "completed_tasks": [],
            "total_commits": 0,
            "last_commit_time": None
        }

    def _save_state(self) -> None:
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def _load_roadmap(self) -> List[Dict[str, Any]]:
        if self.roadmap_file.exists():
            try:
                with open(self.roadmap_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the next pending task from the roadmap.
        """
        idx = self.state.get("current_task_index", 0)
        if idx < len(self.roadmap):
            return self.roadmap[idx]
        return None

    def mark_task_complete(self, task_id: str, commit_hash: Optional[str] = None) -> None:
        """
        Records completion of a roadmap task and advances the index.
        """
        self.state["completed_tasks"].append({
            "id": task_id,
            "commit_hash": commit_hash,
            "index": self.state["current_task_index"]
        })
        self.state["current_task_index"] += 1
        self.state["total_commits"] += 1
        self._save_state()
