"""
Humanizer module to ensure commit messages and code comments look 100% natural,
pragmatic, and human. Strictly forbids emojis, em-dashes, and robotic AI phrasing.
"""
import re
from typing import Optional

# Prohibited patterns
FORBIDDEN_CHARACTERS = [
    "—",  # em-dash
    "–",  # en-dash (often misused)
    "🚀", "✨", "🔥", "⚡", "💡", "🎉", "🤖", "📈", "🛠️", "🔧", "🐛", "📝"  # emojis
]

AI_FLUFF_PATTERNS = [
    r"^this commit (implements|adds|fixes|updates|refactors)",
    r"^in this (commit|pr|pull request)",
    r"comprehensive (suite|tests|refactoring|overhaul)",
    r"for better (clarity|maintainability|readability|performance)",
    r"as requested",
    r"seamless(ly)?",
    r"robust(ly)?",
    r"cutting-edge",
    r"state-of-the-art",
    r"meticulous(ly)?"
]

def clean_commit_message(message: str) -> str:
    """
    Sanitizes and humanizes a commit message.
    - Removes emojis and non-standard dashes.
    - Strips robotic AI preambles.
    - Normalizes casing and formatting.
    """
    if not message:
        return "chore: update code"
    
    # 1. Strip em-dashes and en-dashes, replace with standard hyphen or colon
    clean = message.replace("—", " - ").replace("–", " - ")
    
    # 2. Strip emojis and unicode symbols
    # Remove surrogate pairs / common emoji blocks
    clean = re.sub(r'[\U00010000-\U0010ffff]', '', clean)
    for char in FORBIDDEN_CHARACTERS:
        clean = clean.replace(char, "")
    
    # 3. Clean whitespace
    lines = [line.strip() for line in clean.split("\n") if line.strip()]
    if not lines:
        return "chore: update repository files"
    
    header = lines[0]
    
    # 4. Remove AI fluff phrases from header
    for pattern in AI_FLUFF_PATTERNS:
        header = re.sub(pattern, "", header, flags=re.IGNORECASE).strip()
        header = re.sub(r"^[,\-:\s]+", "", header).strip()
    
    # 5. Ensure valid conventional commit format or standard concise phrase
    valid_prefixes = ["feat", "fix", "refactor", "test", "docs", "perf", "chore", "style", "build", "ci"]
    has_prefix = any(header.lower().startswith(p) for p in valid_prefixes)
    
    if not has_prefix:
        # If it doesn't have a prefix, standardize it to lowercase imperative
        header = header[0].lower() + header[1:] if len(header) > 0 else header
    else:
        # Ensure lowercase after colon
        parts = header.split(":", 1)
        if len(parts) == 2:
            prefix, summary = parts[0].strip().lower(), parts[1].strip()
            if summary:
                summary = summary[0].lower() + summary[1:]
            header = f"{prefix}: {summary}"
    
    # 6. Ensure header is concise (max 72 chars ideally, trim if excessive)
    if len(header) > 78:
        # Try cutting at word boundary
        header = header[:75].rsplit(' ', 1)[0]
        
    # Reassemble (single line or brief 2-line if meaningful body exists)
    if len(lines) > 1:
        body = lines[1]
        for pattern in AI_FLUFF_PATTERNS:
            body = re.sub(pattern, "", body, flags=re.IGNORECASE).strip()
        body = body.replace("—", " - ").replace("–", " - ")
        body = re.sub(r"^[,\-:\.\s]+", "", body).strip()
        body = re.sub(r"[\.\s]+$", "", body).strip()
        if len(body) > 5:
            return f"{header}\n\n{body}"
    
    return header

def validate_human_text(text: str) -> bool:
    """
    Returns True if text meets all humanization criteria (no emojis, no em-dashes).
    """
    if "—" in text:
        return False
    if re.search(r'[\U00010000-\U0010ffff]', text):
        return False
    return True
