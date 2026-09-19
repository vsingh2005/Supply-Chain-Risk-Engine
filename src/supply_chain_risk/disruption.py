from collections import deque
from typing import Dict, List

class DisruptionCascadeSimulator:
    def __init__(self):
        self.dependencies: Dict[str, List[str]] = {}
        self.lead_times: Dict[str, int] = {}

    def add_dependency(self, upstream_supplier_id: str, downstream_node_id: str, lead_time_days: int = 7):
        if upstream_supplier_id not in self.dependencies:
            self.dependencies[upstream_supplier_id] = []
        self.dependencies[upstream_supplier_id].append(downstream_node_id)
        self.lead_times[f"{upstream_supplier_id}->{downstream_node_id}"] = lead_time_days

    def simulate_failure(self, failed_supplier_ids: List[str]) -> Dict[str, int]:
        impacted_day: Dict[str, int] = {s: 0 for s in failed_supplier_ids}
        queue = deque(failed_supplier_ids)
        while queue:
            curr = queue.popleft()
            curr_day = impacted_day[curr]
            for downstream in self.dependencies.get(curr, []):
                edge_key = f"{curr}->{downstream}"
                arrival_day = curr_day + self.lead_times.get(edge_key, 7)
                if downstream not in impacted_day or arrival_day < impacted_day[downstream]:
                    impacted_day[downstream] = arrival_day
                    queue.append(downstream)
        return impacted_day
