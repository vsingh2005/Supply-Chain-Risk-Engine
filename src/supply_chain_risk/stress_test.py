from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class StressScenario:
    scenario_name: str
    demand_surge_factor: float = 1.0
    lead_time_multiplier: float = 1.0
    cost_increase_pct: float = 0.0
    supplier_capacity_reduction_pct: float = 0.0

class StressTestRunner:
    def __init__(self):
        self.scenarios: Dict[str, StressScenario] = {}

    def add_scenario(self, scenario: StressScenario):
        self.scenarios[scenario.scenario_name] = scenario

    def evaluate_node(self, node_id: str, baseline_cost: float, baseline_lead_time: float) -> List[Dict[str, Any]]:
        results = []
        for name, sc in self.scenarios.items():
            stressed_cost = baseline_cost * (1.0 + (sc.cost_increase_pct / 100.0))
            stressed_lead_time = baseline_lead_time * sc.lead_time_multiplier
            cost_impact = stressed_cost - baseline_cost
            results.append({
                "scenario": name,
                "node_id": node_id,
                "stressed_cost": round(stressed_cost, 2),
                "stressed_lead_time": round(stressed_lead_time, 2),
                "cost_delta": round(cost_impact, 2)
            })
        return results
