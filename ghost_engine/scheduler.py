"""
Scheduler, timing jitter, and burst session calculator for authentic human contribution patterns.
"""
import random
import time
from datetime import datetime
import zoneinfo
from typing import Tuple

# Natural hourly productivity weightings (EST)
# Higher weight = more realistic coding activity (afternoons & evenings)
HOURLY_WEIGHTS = {
    0: 0.25,   # 12 AM - late night burst
    1: 0.10,   # 1 AM - rare late night
    2: 0.02,   # 2 AM - sleeping
    3: 0.00,   # 3 AM - sleeping
    4: 0.00,   # 4 AM - sleeping
    5: 0.00,   # 5 AM - sleeping
    6: 0.00,   # 6 AM - sleeping
    7: 0.05,   # 7 AM - rare early morning
    8: 0.15,   # 8 AM - morning start
    9: 0.30,   # 9 AM - morning work
    10: 0.50,  # 10 AM - productive morning
    11: 0.65,  # 11 AM - peak morning
    12: 0.40,  # 12 PM - lunch break dip
    13: 0.60,  # 1 PM - afternoon session
    14: 0.80,  # 2 PM - peak afternoon
    15: 0.85,  # 3 PM - peak afternoon
    16: 0.80,  # 4 PM - afternoon coding
    17: 0.60,  # 5 PM - winding down / dinner
    18: 0.45,  # 6 PM - dinner break
    19: 0.70,  # 7 PM - evening session start
    20: 0.90,  # 8 PM - peak evening flow
    21: 0.95,  # 9 PM - peak evening flow
    22: 0.85,  # 10 PM - evening flow
    23: 0.60,  # 11 PM - late night wrap up
}

def should_execute_now(
    timezone_str: str = "US/Eastern",
    base_activity_factor: float = 0.85
) -> Tuple[bool, str]:
    """
    Evaluates whether the ghost developer should execute using human circadian probability weights.
    """
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        now = datetime.now(tz)
    except Exception:
        now = datetime.now()
        
    hour = now.hour
    weight = HOURLY_WEIGHTS.get(hour, 0.5)
    
    # Combined acceptance probability
    prob = weight * base_activity_factor
    roll = random.random()
    
    if roll > prob:
        return False, f"Circadian gate: Off-cycle at {now.strftime('%I:%M %p %Z')} (roll={roll:.2f} > prob={prob:.2f})"
        
    return True, f"Active coding window approved ({now.strftime('%A %I:%M %p %Z')}, weight={weight:.2f})"

def determine_session_burst_size() -> int:
    """
    Determines how many commits to make in this coding session (1, 2, or 3).
    Humans frequently commit in small bursts (e.g. core logic -> tests -> docs/cleanup).
    """
    roll = random.random()
    if roll < 0.45:
        return 1  # 45% single focused commit
    elif roll < 0.85:
        return 2  # 40% dual commit (feature + tests)
    else:
        return 3  # 15% intense 3-commit flow

def calculate_intra_session_delay_seconds() -> int:
    """
    Calculates realistic pause between related commits in a single session (60s to 300s).
    """
    return random.randint(60, 240)

def calculate_jitter_seconds(max_minutes: int = 35) -> int:
    """
    Calculates a stochastic delay in seconds so commits land on organic minutes (e.g. 2:14, 8:47).
    """
    return random.randint(30, max_minutes * 60)

def apply_jitter(max_minutes: int = 35, verbose: bool = True) -> None:
    """
    Applies random sleep jitter before executing code modifications.
    """
    delay = calculate_jitter_seconds(max_minutes)
    if verbose:
        print(f"[Ghost Scheduler] Applying organic jitter delay of {delay // 60}m {delay % 60}s...")
    time.sleep(delay)
