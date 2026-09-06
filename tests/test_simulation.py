"""
Unit tests for demand simulator.
"""
import numpy as np
from supply_chain_risk.simulation import DemandSimulator

def test_simulate_gbm_shape_and_positivity():
    sim = DemandSimulator(seed=42)
    paths = sim.simulate_gbm(s0=100.0, mu=0.05, sigma=0.2, n_days=10, n_paths=50)
    assert paths.shape == (50, 10)
    assert np.all(paths > 0)

def test_simulate_poisson_distribution():
    sim = DemandSimulator(seed=42)
    paths = sim.simulate_poisson(lam=25.0, n_days=5, n_paths=200)
    assert paths.shape == (200, 5)
    assert np.isclose(np.mean(paths), 25.0, atol=2.0)
