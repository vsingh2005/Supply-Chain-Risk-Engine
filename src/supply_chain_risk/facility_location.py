"""
Capacitated Facility Location Problem (CFLP) solver using PuLP.
"""
import pulp
from typing import List, Dict, Any

class FacilityLocationSolver:
    @staticmethod
    def solve(
        facilities: List[Dict[str, Any]],
        demands: List[Dict[str, Any]],
        cost_matrix: List[List[float]]
    ) -> Dict[str, Any]:
        num_f = len(facilities)
        num_d = len(demands)

        prob = pulp.LpProblem("CFLP", pulp.LpMinimize)
        y = [pulp.LpVariable(f"open_{i}", cat=pulp.LpBinary) for i in range(num_f)]
        x = [[pulp.LpVariable(f"flow_{i}_{j}", lowBound=0) for j in range(num_d)] for i in range(num_f)]

        # Objective
        prob += (
            pulp.lpSum([facilities[i]["fixed_cost"] * y[i] for i in range(num_f)]) +
            pulp.lpSum([cost_matrix[i][j] * x[i][j] for i in range(num_f) for j in range(num_d)])
        )

        # Satisfy demand
        for j in range(num_d):
            prob += pulp.lpSum([x[i][j] for i in range(num_f)]) == demands[j]["demand"]

        # Capacity constraints
        for i in range(num_f):
            prob += pulp.lpSum([x[i][j] for j in range(num_d)]) <= facilities[i]["capacity"] * y[i]

        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        status = pulp.LpStatus[prob.status]
        opened = [facilities[i]["name"] for i in range(num_f) if pulp.value(y[i]) > 0.5]

        return {
            "status": status,
            "total_cost": float(pulp.value(prob.objective)),
            "opened_facilities": opened
        }
