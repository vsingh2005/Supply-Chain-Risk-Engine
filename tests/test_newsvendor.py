from supply_chain_risk.newsvendor import ConstrainedNewsvendor

def test_constrained_newsvendor():
    products = [
        {"name": "ItemA", "sale_price": 50.0, "cost": 20.0, "salvage_value": 5.0, "mean_demand": 100, "demand_std": 20},
        {"name": "ItemB", "sale_price": 80.0, "cost": 40.0, "salvage_value": 10.0, "mean_demand": 50, "demand_std": 10},
    ]
    nv = ConstrainedNewsvendor(products)
    unconstrained = nv.solve_unconstrained()
    assert unconstrained["ItemA"] > 90
    constrained = nv.solve_with_budget(total_budget=1000.0)
    total_spent = sum(constrained[p["name"]] * p["cost"] for p in products)
    assert total_spent <= 1005.0
