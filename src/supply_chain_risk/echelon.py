"""
Multi-echelon serial inventory base-stock policy calculator.
"""
import numpy as np
from typing import List, Dict, Any

class MultiEchelonOptimizer:
    """
    Computes Clark-Scarf echelon inventory positions for serial supply chains.
    """
    def __init__(self, stages: List[str], holding_costs: List[float], lead_times: List[float]):
        if not (len(stages) == len(holding_costs) == len(lead_times)):
            raise ValueError("Stages, holding costs, and lead times must match in length")
        self.stages = stages
        self.holding_costs = np.array(holding_costs, dtype=np.float64)
        self.lead_times = np.array(lead_times, dtype=np.float64)

    def compute_echelon_holding_costs(self) -> np.ndarray:
        # e_i = h_i - h_{i+1}
        echelon_h = np.zeros_like(self.holding_costs)
        for i in range(len(self.holding_costs)):
            next_h = self.holding_costs[i + 1] if i + 1 < len(self.holding_costs) else 0.0
            echelon_h[i] = max(0.01, self.holding_costs[i] - next_h)
        return echelon_h

    def recommend_base_stock(self, mean_demand: float, demand_std: float, service_factor_z: float = 1.65) -> Dict[str, Any]:
        results = {}
        cumulative_lt = 0.0
        for i, stage in enumerate(self.stages):
            cumulative_lt += self.lead_times[i]
            pipeline_mean = mean_demand * cumulative_lt
            pipeline_std = demand_std * np.sqrt(cumulative_lt)
            base_stock = pipeline_mean + (service_factor_z * pipeline_std)
            results[stage] = {
                "echelon_holding_cost": round(float(self.compute_echelon_holding_costs()[i]), 3),
                "recommended_base_stock": int(np.ceil(base_stock)),
                "cumulative_lead_time": cumulative_lt
            }
        return results
