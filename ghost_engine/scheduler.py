"""
Scheduler and jitter calculator for realistic human contribution patterns.
"""
import random
import time
from datetime import datetime
import zoneinfo
from typing import Tuple

def should_execute_now(
    timezone_str: str = "US/Eastern",
    min_hour: int = 10,
    max_hour: int = 23,
    skip_prob: float = 0.20
) -> Tuple[bool, str]:
    """
    Evaluates whether the ghost developer should execute at the current moment based on:
    1. Realistic human waking hours in target timezone
    2. Random probability skip (to avoid unnatural daily robot streaks)
    """
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        now = datetime.now(tz)
    except Exception:
        now = datetime.now()
        
    hour = now.hour
    weekday = now.weekday()  # 0 is Monday, 6 is Sunday
    
    # Check hours
    if hour < min_hour or hour > max_hour:
        return False, f"Outside active developer hours ({min_hour}:00 - {max_hour}:00 {timezone_str}). Current hour: {hour}"
    
    # Higher chance to skip on weekends (Saturday=5, Sunday=6)
    effective_skip_prob = skip_prob * 1.5 if weekday in (5, 6) else skip_prob
    
    if random.random() < effective_skip_prob:
        return False, f"Simulated off-day / break (random skip triggered with p={effective_skip_prob:.2f})"
        
    return True, f"Active window approved ({now.strftime('%A %I:%M %p %Z')})"

def calculate_jitter_seconds(max_minutes: int = 45) -> int:
    """
    Calculates a stochastic delay in seconds to ensure commits aren't clustered at :00 cron marks.
    """
    return random.randint(10, max_minutes * 60)

def apply_jitter(max_minutes: int = 45, verbose: bool = True) -> None:
    """
    Applies random sleep jitter before executing code modifications.
    """
    delay = calculate_jitter_seconds(max_minutes)
    if verbose:
        print(f"[Ghost Scheduler] Applying jitter delay of {delay // 60}m {delay % 60}s for organic timing...")
    time.sleep(delay)
