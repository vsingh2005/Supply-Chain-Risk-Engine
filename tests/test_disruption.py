from supply_chain_risk.disruption import DisruptionCascadeSimulator

def test_disruption_cascade_propagation():
    sim = DisruptionCascadeSimulator()
    sim.add_dependency("raw_silicon", "mcu_fab", lead_time_days=14)
    sim.add_dependency("mcu_fab", "ecu_assembly", lead_time_days=7)
    sim.add_dependency("ecu_assembly", "car_factory", lead_time_days=3)
    impact = sim.simulate_failure(["raw_silicon"])
    assert impact["raw_silicon"] == 0
    assert impact["mcu_fab"] == 14
    assert impact["ecu_assembly"] == 21
    assert impact["car_factory"] == 24
