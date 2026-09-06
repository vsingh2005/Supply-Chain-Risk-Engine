"""
Unit tests for supply chain models.
"""
from supply_chain_risk.models import Node, Supplier

def test_node_creation():
    node = Node(
        node_id="WH-01",
        name="Amherst Distribution Center",
        capacity=50000.0,
        holding_cost_per_unit=2.5,
        stockout_penalty_per_unit=12.0
    )
    assert node.node_id == "WH-01"
    assert node.capacity == 50000.0
    assert node.holding_cost_per_unit == 2.5

def test_supplier_creation():
    supplier = Supplier(
        supplier_id="SUP-NE",
        name="Northeast Component Labs",
        base_lead_time_days=7.0,
        lead_time_std_dev=1.5,
        disruption_probability=0.02,
        unit_cost=45.0
    )
    assert supplier.supplier_id == "SUP-NE"
    assert supplier.disruption_probability == 0.02
