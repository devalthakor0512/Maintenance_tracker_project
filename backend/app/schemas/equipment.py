from pydantic import BaseModel
from typing import Optional
from datetime import date
from .team import TeamResponse
from .user import UserResponse

class EquipmentBase(BaseModel):
    equipment_name: str
    serial_number: str
    category: str
    department: str
    location: str
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    notes: Optional[str] = None
    status: str = "active"

class EquipmentCreate(EquipmentBase):
    assigned_employee_id: Optional[int] = None
    maintenance_team_id: Optional[int] = None

class EquipmentResponse(EquipmentBase):
    id: int
    assigned_employee_id: Optional[int] = None
    maintenance_team_id: Optional[int] = None
    
    # Relationships (Optional to avoid recursion depth if needed, but good for display)
    assigned_to: Optional[UserResponse] = None
    team: Optional[TeamResponse] = None

    class Config:
        from_attributes = True
