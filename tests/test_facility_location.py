from supply_chain_risk.facility_location import FacilityLocationSolver

def test_facility_location_solver():
    facilities = [
        {"name": "Boston_DC", "fixed_cost": 5000, "capacity": 500},
        {"name": "Jersey_DC", "fixed_cost": 3000, "capacity": 300},
    ]
    demands = [
        {"name": "Store1", "demand": 150},
        {"name": "Store2", "demand": 100},
    ]
    cost_matrix = [
        [10.0, 15.0],
        [20.0, 5.0]
    ]
    res = FacilityLocationSolver.solve(facilities, demands, cost_matrix)
    assert res["status"] == "Optimal"
    assert len(res["opened_facilities"]) > 0
