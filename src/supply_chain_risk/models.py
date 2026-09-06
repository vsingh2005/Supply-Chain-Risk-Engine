from pydantic import BaseModel, Field

class Node(BaseModel):
    node_id: str
    name: str
    capacity: float = Field(..., gt=0)
    holding_cost_per_unit: float = Field(default=1.0, ge=0)
    stockout_penalty_per_unit: float = Field(default=5.0, ge=0)

class Supplier(BaseModel):
    supplier_id: str
    name: str
    base_lead_time_days: float = Field(..., gt=0)
    lead_time_std_dev: float = Field(default=1.0, ge=0)
    disruption_probability: float = Field(default=0.05, ge=0.0, le=1.0)
    unit_cost: float = Field(..., gt=0)
