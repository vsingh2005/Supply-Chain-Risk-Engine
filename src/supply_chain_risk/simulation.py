"""
Monte Carlo stochastic demand simulation engine.
"""
import numpy as np
from typing import List, Optional

class DemandSimulator:
    """
    Simulates demand time series using Geometric Brownian Motion or Poisson arrivals.
    """
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)

    def simulate_gbm(
        self,
        s0: float,
        mu: float,
        sigma: float,
        n_days: int = 30,
        n_paths: int = 1000
    ) -> np.ndarray:
        """
        Simulates Geometric Brownian Motion demand paths.
        Returns array of shape (n_paths, n_days).
        """
        dt = 1.0 / n_days
        paths = np.zeros((n_paths, n_days))
        paths[:, 0] = s0
        
        for t in range(1, n_days):
            z = self.rng.standard_normal(n_paths)
            paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
            
        return paths

    def simulate_poisson(
        self,
        lam: float,
        n_days: int = 30,
        n_paths: int = 1000
    ) -> np.ndarray:
        """
        Simulates discrete Poisson daily customer arrival demand.
        """
        return self.rng.poisson(lam=lam, size=(n_paths, n_days))
