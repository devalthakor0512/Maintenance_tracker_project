from pydantic import BaseModel
from typing import List, Optional
from .user import UserResponse

class TeamBase(BaseModel):
    team_name: str

class TeamCreate(TeamBase):
    members: Optional[List[int]] = []

class TeamResponse(TeamBase):
    id: int
    members: List[UserResponse] = []

    class Config:
        from_attributes = True
