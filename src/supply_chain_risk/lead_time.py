import numpy as np
from typing import Optional

class LeadTimeSimulator:
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)

    def sample_lognormal(self, mean_days: float, sigma: float = 0.35, size: int = 1000) -> np.ndarray:
        mu = np.log(mean_days) - (0.5 * sigma**2)
        samples = self.rng.lognormal(mean=mu, sigma=sigma, size=size)
        return np.maximum(1.0, np.round(samples, 1))

    def sample_weibull(self, scale_days: float, shape: float = 2.0, size: int = 1000) -> np.ndarray:
        samples = scale_days * self.rng.weibull(a=shape, size=size)
        return np.maximum(1.0, np.round(samples, 1))
