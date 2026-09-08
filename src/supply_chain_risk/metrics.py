import numpy as np
from typing import Tuple

def compute_var_cvar(losses: np.ndarray, alpha: float = 0.95) -> Tuple[float, float]:
    if len(losses) == 0:
        raise ValueError("Losses array cannot be empty")
    sorted_losses = np.sort(losses)
    idx = int(np.ceil(alpha * len(sorted_losses))) - 1
    var = float(sorted_losses[idx])
    tail_losses = sorted_losses[idx:]
    cvar = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var
    return var, cvar
