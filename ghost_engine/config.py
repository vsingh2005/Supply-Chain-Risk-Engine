"""
Configuration settings for the Ghost Developer Engine.
"""
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class GhostConfig:
    # Git Author Details (configured via environment variables or defaults)
    git_author_name: str = os.getenv("GHOST_GIT_NAME", "Ghost Developer")
    git_author_email: str = os.getenv("GHOST_GIT_EMAIL", "ghost.developer@example.com")
    
    # LLM API configuration (optional - falls back to deterministic roadmaps if not set)
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    
    # Scheduling & Timing
    timezone: str = os.getenv("GHOST_TIMEZONE", "US/Eastern")
    min_hour: int = int(os.getenv("GHOST_MIN_HOUR", "10"))  # 10 AM EST
    max_hour: int = int(os.getenv("GHOST_MAX_HOUR", "23"))  # 11 PM EST
    skip_probability: float = float(os.getenv("GHOST_SKIP_PROB", "0.20"))  # 20% chance to skip for human realism
    max_commits_per_run: int = int(os.getenv("GHOST_MAX_COMMITS", "2"))
    
    # GitHub Token (for pushing if run in central orchestrator mode)
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN", None)
    
    # Target Repositories
    repos: List[str] = field(default_factory=lambda: [
        "fleet-telemetry-pipeline",
        "supply-chain-risk-engine",
        "edge-tensor-quantizer"
    ])
