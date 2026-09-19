import numpy as np
from supply_chain_risk.lead_time import LeadTimeSimulator

def test_lead_time_distributions():
    sim = LeadTimeSimulator(seed=123)
    lognorm_days = sim.sample_lognormal(mean_days=14.0, size=500)
    assert len(lognorm_days) == 500
    assert np.all(lognorm_days >= 1.0)
    assert 10.0 <= np.mean(lognorm_days) <= 18.0

    weibull_days = sim.sample_weibull(scale_days=20.0, size=500)
    assert len(weibull_days) == 500
    assert np.all(weibull_days >= 1.0)
