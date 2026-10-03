"""
Freight container knapsack packing optimization.
"""
from typing import List, Dict, Any

class FreightKnapsackOptimizer:
    @staticmethod
    def optimize_packing(
        items: List[Dict[str, Any]],
        max_weight_kg: int,
        max_volume_m3: int
    ) -> Dict[str, Any]:
        """
        0-1 multidimensional knapsack using recursive memoized DP.
        """
        memo = {}
        def dp(i: int, w_rem: int, v_rem: int) -> float:
            if i >= len(items) or w_rem <= 0 or v_rem <= 0:
                return 0.0
            state = (i, w_rem, v_rem)
            if state in memo:
                return memo[state]

            # Option 1: Skip
            best = dp(i + 1, w_rem, v_rem)

            # Option 2: Take if fits
            it = items[i]
            if it["weight"] <= w_rem and it["volume"] <= v_rem:
                take = it["value"] + dp(i + 1, w_rem - it["weight"], v_rem - it["volume"])
                if take > best:
                    best = take

            memo[state] = best
            return best

        val = dp(0, max_weight_kg, max_volume_m3)
        return {
            "max_value": val,
            "max_weight_kg": max_weight_kg,
            "max_volume_m3": max_volume_m3
        }
