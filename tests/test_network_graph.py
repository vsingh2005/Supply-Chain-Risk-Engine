from supply_chain_risk.network_graph import SupplyNetworkGraph

def test_supply_network_graph():
    g = SupplyNetworkGraph()
    g.add_edge("Tier2_A", "Tier1_Hub")
    g.add_edge("Tier2_B", "Tier1_Hub")
    g.add_edge("Tier1_Hub", "Assembly_Plant_1")
    g.add_edge("Tier1_Hub", "Assembly_Plant_2")

    order = g.topological_sort()
    assert order[0].startswith("Tier2")
    assert order[-1].startswith("Assembly")

    bottlenecks = g.find_critical_bottlenecks()
    assert bottlenecks[0] == "Tier1_Hub"
