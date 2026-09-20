import math
from typing import Dict, Any

class EOQOptimizer:
    @staticmethod
    def calculate_classic_eoq(annual_demand: float, order_cost: float, holding_cost_per_unit_year: float) -> Dict[str, Any]:
        if annual_demand <= 0 or order_cost <= 0 or holding_cost_per_unit_year <= 0:
            raise ValueError("All inputs must be strictly positive")
        q_star = math.sqrt((2.0 * annual_demand * order_cost) / holding_cost_per_unit_year)
        orders_per_year = annual_demand / q_star
        annual_order_cost = orders_per_year * order_cost
        annual_holding_cost = (q_star / 2.0) * holding_cost_per_unit_year
        total_annual_cost = annual_order_cost + annual_holding_cost
        return {
            "optimal_order_quantity": round(q_star, 1),
            "orders_per_year": round(orders_per_year, 2),
            "annual_order_cost": round(annual_order_cost, 2),
            "annual_holding_cost": round(annual_holding_cost, 2),
            "total_annual_cost": round(total_annual_cost, 2)
        }
