"""
Main Ghost Developer Runner CLI.
Coordinates task execution, schedule verification, git operations, and humanized commits.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from ghost_engine.config import GhostConfig
from ghost_engine.humanizer import clean_commit_message
from ghost_engine.scheduler import (
    should_execute_now,
    apply_jitter,
    determine_session_burst_size,
    calculate_intra_session_delay_seconds
)
import time
from ghost_engine.task_manager import TaskManager
from ghost_engine.generator import CodeGenerator
from ghost_engine.validator import run_repo_tests

def run_git_command(args: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False
    )

def commit_and_push(
    repo_path: Path,
    commit_msg: str,
    author_name: str,
    author_email: str,
    dry_run: bool = False,
    push: bool = True
) -> bool:
    """
    Stages changes, creates a humanized Git commit, and pushes to remote.
    """
    if dry_run:
        print(f"[DRY RUN] Would commit with message: '{commit_msg}'")
        print(f"[DRY RUN] Author: {author_name} <{author_email}>")
        return True
        
    # Stage all changes
    run_git_command(["add", "."], repo_path)
    
    # Check if there are staged changes
    status = run_git_command(["status", "--porcelain"], repo_path)
    if not status.stdout.strip():
        print("[Ghost Runner] No changes detected to commit.")
        return False
        
    # Commit with custom author
    author_flag = f"{author_name} <{author_email}>"
    commit_res = run_git_command([
        "commit",
        "-m", commit_msg,
        f"--author={author_flag}"
    ], repo_path)
    
    if commit_res.returncode != 0:
        print(f"[Ghost Runner] Git commit error:\n{commit_res.stderr}")
        return False
        
    print(f"[Ghost Runner] Successfully committed: {commit_msg}")
    
    if push:
        push_res = run_git_command(["push"], repo_path)
        if push_res.returncode != 0:
            print(f"[Ghost Runner] Git push warning/error:\n{push_res.stderr}")
            return False
        print("[Ghost Runner] Successfully pushed commit to origin.")
        
    return True

def process_repository(
    repo_path: Path,
    config: GhostConfig,
    dry_run: bool = False,
    push: bool = True,
    max_burst: Optional[int] = None
) -> int:
    """
    Advances a single repository by 1 to 3 roadmap tasks in a realistic burst session.
    Returns the number of successful commits.
    """
    if not repo_path.exists():
        print(f"[Ghost Runner] Repo path does not exist: {repo_path}")
        return 0
        
    print(f"\n=======================================================")
    print(f"[Ghost Runner] Processing repository: {repo_path.name}")
    print(f"=======================================================")
    
    task_mgr = TaskManager(str(repo_path))
    generator = CodeGenerator(str(repo_path))
    
    burst_count = max_burst if max_burst is not None else determine_session_burst_size()
    print(f"[Ghost Runner] Active session plan: {burst_count} commit(s)")
    
    successful_commits = 0
    for i in range(burst_count):
        task = task_mgr.get_next_task()
        if not task:
            print(f"[Ghost Runner] No further pending roadmap tasks for {repo_path.name}.")
            break
            
        print(f"\n[Ghost Runner] [{i+1}/{burst_count}] Task: [{task.get('id')}] - {task.get('title')}")
        
        # Apply the code changes
        success, msg, raw_commit_msg = generator.apply_task(task)
        if not success:
            print(f"[Ghost Runner] Task application failed: {msg}")
            break
            
        print(f"[Ghost Runner] {msg}")
        
        # Run test suite validation
        tests_pass, test_msg = run_repo_tests(repo_path)
        if not tests_pass:
            print(f"[Ghost Runner] Pre-commit test failure: {test_msg}")
            run_git_command(["checkout", "."], repo_path)
            break
            
        print(f"[Ghost Runner] Validation passed: {test_msg}")
        
        # Sanitize commit message
        final_commit_msg = clean_commit_message(raw_commit_msg)
        
        # Commit and push
        committed = commit_and_push(
            repo_path=repo_path,
            commit_msg=final_commit_msg,
            author_name=config.git_author_name,
            author_email=config.git_author_email,
            dry_run=dry_run,
            push=push
        )
        
        if committed:
            successful_commits += 1
            if not dry_run:
                task_mgr.mark_task_complete(task.get("id", "task"))
                
            # If multi-commit burst, pause briefly before next commit (unless dry-run)
            if i < burst_count - 1 and not dry_run:
                pause = calculate_intra_session_delay_seconds()
                print(f"[Ghost Runner] Pausing {pause}s before next commit in session...")
                time.sleep(pause)
                
    return successful_commits

def main():
    parser = argparse.ArgumentParser(description="Autonomous Ghost Developer Engine")
    parser.add_argument("--repo", type=str, default=None, help="Target specific repository directory")
    parser.add_argument("--dry-run", action="store_true", help="Execute without modifying git history or pushing")
    parser.add_argument("--force", action="store_true", help="Bypass schedule, active hours, and probability skip gates")
    parser.add_argument("--no-jitter", action="store_true", help="Skip stochastic timing jitter delay")
    parser.add_argument("--no-push", action="store_true", help="Commit locally without pushing to remote")
    
    args = parser.parse_args()
    config = GhostConfig()
    
    # Schedule & active hour checks
    if not args.force and not args.dry_run:
        should_run, reason = should_execute_now(
            timezone_str=config.timezone,
            min_hour=config.min_hour,
            max_hour=config.max_hour,
            skip_prob=config.skip_probability
        )
        if not should_run:
            print(f"[Ghost Scheduler] Execution skipped: {reason}")
            sys.exit(0)
            
        if not args.no_jitter:
            apply_jitter(max_minutes=30)
            
    base_dir = Path(__file__).resolve().parent.parent
    repos_dir = base_dir / "repos"
    
    if args.repo:
        target_path = Path(args.repo).resolve()
        process_repository(target_path, config, dry_run=args.dry_run, push=not args.no_push)
    else:
        # Check repos directory
        if not repos_dir.exists():
            print(f"[Ghost Runner] No repos directory found at {repos_dir}")
            sys.exit(1)
            
        for repo_folder in repos_dir.iterdir():
            if repo_folder.is_dir() and (repo_folder / ".ghost").exists():
                process_repository(repo_folder, config, dry_run=args.dry_run, push=not args.no_push)

if __name__ == "__main__":
    main()
