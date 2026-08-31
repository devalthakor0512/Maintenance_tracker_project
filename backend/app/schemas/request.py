from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .equipment import EquipmentResponse
from .user import UserResponse
from .team import TeamResponse

class RequestBase(BaseModel):
    subject: str
    equipment_id: Optional[int] = None
    request_type: str # "Corrective" or "Preventive"
    scheduled_date: Optional[datetime] = None
    duration: Optional[int] = None # hours
    stage: str = "New" 
    assigned_technician_id: Optional[int] = None

class RequestCreate(RequestBase):
    # User only sends basic info, system auto-fills the rest
    pass

class RequestUpdate(BaseModel):
    subject: Optional[str] = None
    equipment_id: Optional[int] = None
    request_type: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    duration: Optional[int] = None
    stage: Optional[str] = None
    assigned_technician_id: Optional[int] = None

class RequestResponse(RequestBase):
    id: int
    category: Optional[str]
    maintenance_team_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    equipment: Optional[EquipmentResponse] = None
    technician: Optional[UserResponse] = None
    team: Optional[TeamResponse] = None

    class Config:
        from_attributes = True
