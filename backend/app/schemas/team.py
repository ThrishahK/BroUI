from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamBase(BaseModel):
    team_leader_usn: str
    team_name: Optional[str] = None
    is_active: bool = True

class TeamCreate(TeamBase):
    password: str

class TeamUpdate(BaseModel):
    team_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True