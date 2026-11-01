import pytest
from supply_chain_risk.choke_points import ChokePointVulnerabilityEvaluator

def test_choke_point_impact():
    res = ChokePointVulnerabilityEvaluator.calculate_disruption_impact(
        "Suez_Canal",
        shipment_volume_teu=500,
        cargo_value_per_teu=80000.0,
        disruption_duration_days=14.0
    )
    assert res["detour_days"] == 12.0
    assert res["fuel_cost"] == 270000.0
    assert res["inventory_delay_cost"] == 197260.27
    assert res["total_disruption_impact"] == 467260.27

@pytest.mark.parametrize("duration,delay", [(0, 0), (3, 3), (14, 12)])
def test_disruption_duration(duration, delay):
    res = ChokePointVulnerabilityEvaluator.calculate_disruption_impact("Suez_Canal", 500, 80000.0, duration)
    assert res["detour_days"] == delay
    assert res["total_disruption_impact"] == round(500 * delay * 45 + 500 * 80000 * delay / 365 * 0.15, 2)

def test_negative_duration_rejected():
    with pytest.raises(ValueError):
        ChokePointVulnerabilityEvaluator.calculate_disruption_impact("Suez_Canal", 500, 80000, -1)
