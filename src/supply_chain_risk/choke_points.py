"""
Maritime transit choke-point vulnerability calculator (e.g. Suez, Malacca, Panama).
"""
from typing import Dict, Any

CHOKE_POINT_DEFAULTS = {
    "Suez_Canal": {"detour_days": 12.0, "daily_cost_per_teu": 45.0, "global_teu_pct": 12.0},
    "Panama_Canal": {"detour_days": 18.0, "daily_cost_per_teu": 40.0, "global_teu_pct": 5.0},
    "Malacca_Strait": {"detour_days": 6.0, "daily_cost_per_teu": 50.0, "global_teu_pct": 25.0},
}

class ChokePointVulnerabilityEvaluator:
    @staticmethod
    def calculate_disruption_impact(
        choke_point_name: str,
        shipment_volume_teu: int,
        cargo_value_per_teu: float,
        disruption_duration_days: float
    ) -> Dict[str, Any]:
        if min(shipment_volume_teu, cargo_value_per_teu, disruption_duration_days) < 0:
            raise ValueError("Inputs must be nonnegative")
        info = CHOKE_POINT_DEFAULTS.get(choke_point_name, {"detour_days": 10.0, "daily_cost_per_teu": 45.0, "global_teu_pct": 10.0})
        # Route around the closure only when faster than waiting.
        detour_days = min(info["detour_days"], disruption_duration_days)
        fuel_detour_cost = shipment_volume_teu * detour_days * info["daily_cost_per_teu"]
        inventory_delay_cost = shipment_volume_teu * cargo_value_per_teu * (detour_days / 365.0) * 0.15

        total_impact = fuel_detour_cost + inventory_delay_cost
        return {
            "choke_point": choke_point_name,
            "detour_days": detour_days,
            "fuel_cost": round(fuel_detour_cost, 2),
            "inventory_delay_cost": round(inventory_delay_cost, 2),
            "total_disruption_impact": round(total_impact, 2)
        }
