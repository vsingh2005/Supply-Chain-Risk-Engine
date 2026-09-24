from supply_chain_risk.echelon import MultiEchelonOptimizer

def test_multi_echelon_optimizer():
    opt = MultiEchelonOptimizer(
        stages=["Retailer", "Distributor", "Manufacturer"],
        holding_costs=[10.0, 6.0, 2.0],
        lead_times=[2.0, 5.0, 10.0]
    )
    res = opt.recommend_base_stock(mean_demand=100.0, demand_std=15.0)
    assert "Retailer" in res
    assert res["Retailer"]["recommended_base_stock"] > 200
    assert res["Manufacturer"]["cumulative_lead_time"] == 17.0
