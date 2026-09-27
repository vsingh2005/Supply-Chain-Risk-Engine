"""
Constrained multi-product Newsvendor problem solver.
"""
from typing import List, Dict, Any
import numpy as np
from scipy.stats import norm

class ConstrainedNewsvendor:
    def __init__(self, products: List[Dict[str, Any]]):
        self.products = products

    def solve_unconstrained(self) -> Dict[str, float]:
        orders = {}
        for p in self.products:
            cu = p["sale_price"] - p["cost"]
            co = p["cost"] - p.get("salvage_value", 0.0)
            crit_ratio = cu / (cu + co)
            q = norm.ppf(crit_ratio, loc=p["mean_demand"], scale=p["demand_std"])
            orders[p["name"]] = max(0.0, float(round(q, 1)))
        return orders

    def solve_with_budget(self, total_budget: float) -> Dict[str, float]:
        unconstrained = self.solve_unconstrained()
        total_cost = sum(unconstrained[p["name"]] * p["cost"] for p in self.products)
        if total_cost <= total_budget or total_cost == 0:
            return unconstrained
        scale = total_budget / total_cost
        return {p["name"]: round(unconstrained[p["name"]] * scale, 1) for p in self.products}
