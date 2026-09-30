import numpy as np
from supply_chain_risk.copula import CorrelatedLeadTimeSimulator

def test_copula_correlation():
    copula = CorrelatedLeadTimeSimulator(correlation_rho=0.8)
    lt1, lt2 = copula.sample_lead_times(n_samples=500, mean_lt1=14.0, std_lt1=3.0, mean_lt2=21.0, std_lt2=5.0)
    assert len(lt1) == 500
    corr = np.corrcoef(lt1, lt2)[0, 1]
    assert 0.7 < corr < 0.9
