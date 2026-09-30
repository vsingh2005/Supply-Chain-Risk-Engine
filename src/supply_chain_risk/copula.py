"""
Bivariate Gaussian copula for simulating correlated supplier disruptions.
"""
import numpy as np
from scipy.stats import norm, lognorm
from typing import Tuple

class CorrelatedLeadTimeSimulator:
    def __init__(self, correlation_rho: float = 0.6):
        if not (-1.0 <= correlation_rho <= 1.0):
            raise ValueError("Correlation rho must be in [-1, 1]")
        self.rho = correlation_rho

    def sample_lead_times(
        self,
        n_samples: int,
        mean_lt1: float, std_lt1: float,
        mean_lt2: float, std_lt2: float,
        seed: int = 42
    ) -> Tuple[np.ndarray, np.ndarray]:
        rng = np.random.RandomState(seed)
        mean = [0, 0]
        cov = [[1.0, self.rho], [self.rho, 1.0]]
        z = rng.multivariate_normal(mean, cov, size=n_samples)
        u1 = norm.cdf(z[:, 0])
        u2 = norm.cdf(z[:, 1])

        # Map uniforms to normal lead time distributions
        lt1 = norm.ppf(np.clip(u1, 1e-5, 1 - 1e-5), loc=mean_lt1, scale=std_lt1)
        lt2 = norm.ppf(np.clip(u2, 1e-5, 1 - 1e-5), loc=mean_lt2, scale=std_lt2)
        return np.maximum(1.0, lt1), np.maximum(1.0, lt2)
