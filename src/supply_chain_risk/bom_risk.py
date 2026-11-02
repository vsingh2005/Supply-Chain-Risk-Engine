"""
Multi-tier Bill of Materials (BOM) risk analyzer.
"""
from typing import Dict, List, Any

class BOMRiskAnalyzer:
    def __init__(self, bom_tree: Dict[str, Any]):
        self.bom = bom_tree

    def find_single_source_components(self) -> List[Dict[str, Any]]:
        vulnerabilities = []
        def traverse(node: Dict[str, Any], path: str):
            suppliers = node.get("suppliers", [])
            if len(suppliers) == 1:
                vulnerabilities.append({
                    "component": node.get("name"),
                    "path": path,
                    "supplier": suppliers[0],
                    "lead_time_weeks": node.get("lead_time_weeks", 4)
                })
            for sub in node.get("sub_components", []):
                traverse(sub, f"{path} -> {sub.get('name')}")

        traverse(self.bom, self.bom.get("name", "Product"))
        return vulnerabilities
