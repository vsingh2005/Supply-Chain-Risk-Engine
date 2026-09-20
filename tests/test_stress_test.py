from supply_chain_risk.stress_test import StressScenario, StressTestRunner

def test_stress_test_scenario_execution():
    runner = StressTestRunner()
    runner.add_scenario(StressScenario(
        scenario_name="corridor_embargo",
        lead_time_multiplier=2.5,
        cost_increase_pct=35.0
    ))
    runner.add_scenario(StressScenario(
        scenario_name="normal_operations",
        lead_time_multiplier=1.0,
        cost_increase_pct=0.0
    ))
    res = runner.evaluate_node("port_rotterdam", baseline_cost=10000.0, baseline_lead_time=12.0)
    assert len(res) == 2
    embargo = next(r for r in res if r["scenario"] == "corridor_embargo")
    assert embargo["stressed_cost"] == 13500.0
    assert embargo["stressed_lead_time"] == 30.0
