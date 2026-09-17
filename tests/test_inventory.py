from supply_chain_risk.inventory import InventoryPolicyOptimizer

def test_safety_stock_and_reorder_point():
    policy = InventoryPolicyOptimizer.compute_policy(
        avg_lead_time_days=10.0,
        std_lead_time_days=2.0,
        avg_daily_demand=100.0,
        std_daily_demand=15.0,
        service_level=0.95
    )
    assert policy["expected_lead_time_demand"] == 1000.0
    assert policy["safety_stock"] > 0
    assert policy["reorder_point"] > policy["expected_lead_time_demand"]
