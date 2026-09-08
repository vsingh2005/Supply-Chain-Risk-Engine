import numpy as np
from supply_chain_risk.metrics import compute_var_cvar

def test_var_cvar_calculation():
    losses = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    var, cvar = compute_var_cvar(losses, alpha=0.90)
    assert var == 90.0 and cvar == 95.0
