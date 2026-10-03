from supply_chain_risk.knapsack import FreightKnapsackOptimizer

def test_knapsack_freight():
    items = [
        {"name": "Electronics", "weight": 200, "volume": 10, "value": 5000},
        {"name": "Apparel", "weight": 100, "volume": 20, "value": 2000},
        {"name": "Machinery", "weight": 500, "volume": 15, "value": 8000},
    ]
    res = FreightKnapsackOptimizer.optimize_packing(items, max_weight_kg=600, max_volume_m3=25)
    assert res["max_value"] >= 8000
