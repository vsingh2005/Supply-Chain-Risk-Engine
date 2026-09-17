import math
from typing import Dict, Any

class InventoryPolicyOptimizer:
    SERVICE_LEVEL_Z = {
        0.90: 1.282,
        0.95: 1.645,
        0.98: 2.054,
        0.99: 2.326,
        0.999: 3.090,
    }

    @classmethod
    def calculate_safety_stock(
        cls,
        avg_lead_time_days: float,
        std_lead_time_days: float,
        avg_daily_demand: float,
        std_daily_demand: float,
        service_level: float = 0.95
    ) -> float:
        z = cls.SERVICE_LEVEL_Z.get(service_level, 1.645)
        variance = (avg_lead_time_days * (std_daily_demand ** 2)) + ((avg_daily_demand ** 2) * (std_lead_time_days ** 2))
        return float(z * math.sqrt(variance))

    @classmethod
    def compute_policy(
        cls,
        avg_lead_time_days: float,
        std_lead_time_days: float,
        avg_daily_demand: float,
        std_daily_demand: float,
        service_level: float = 0.95
    ) -> Dict[str, Any]:
        safety_stock = cls.calculate_safety_stock(
            avg_lead_time_days, std_lead_time_days, avg_daily_demand, std_daily_demand, service_level
        )
        lead_time_demand = avg_daily_demand * avg_lead_time_days
        reorder_point = lead_time_demand + safety_stock
        return {
            "service_level": service_level,
            "safety_stock": round(safety_stock, 2),
            "expected_lead_time_demand": round(lead_time_demand, 2),
            "reorder_point": round(reorder_point, 2)
        }
