"""
Supply chain network digraph and topological bottleneck analyzer.
"""
from typing import Dict, List, Set

class SupplyNetworkGraph:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}
        self.in_degree: Dict[str, int] = {}
        self.nodes: Set[str] = set()

    def add_edge(self, source: str, target: str):
        self.nodes.add(source)
        self.nodes.add(target)
        if source not in self.adj:
            self.adj[source] = []
        self.adj[source].append(target)
        self.in_degree[target] = self.in_degree.get(target, 0) + 1
        if source not in self.in_degree:
            self.in_degree[source] = 0

    def topological_sort(self) -> List[str]:
        in_deg = dict(self.in_degree)
        queue = [n for n in self.nodes if in_deg.get(n, 0) == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in self.adj.get(node, []):
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)
        if len(order) != len(self.nodes):
            raise ValueError("Graph contains a cycle")
        return order

    def find_critical_bottlenecks(self) -> List[str]:
        # Nodes with high fan-in and fan-out
        scored = []
        for n in self.nodes:
            in_d = self.in_degree.get(n, 0)
            out_d = len(self.adj.get(n, []))
            scored.append((n, in_d * out_d))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [node for node, score in scored if score > 0]
