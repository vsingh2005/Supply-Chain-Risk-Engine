from supply_chain_risk.eoq import EOQOptimizer

def test_classic_eoq_calculation():
    res = EOQOptimizer.calculate_classic_eoq(10000, 50, 4)
    assert res["optimal_order_quantity"] == 500.0
    assert res["orders_per_year"] == 20.0
    assert res["annual_order_cost"] == 1000.0
    assert res["annual_holding_cost"] == 1000.0
    assert res["total_annual_cost"] == 2000.0
