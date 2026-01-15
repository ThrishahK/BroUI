from pydantic import BaseModel, Field
from typing import Optional

class TeamLogin(BaseModel):
    team_leader_usn: str = Field(..., description="Team Leader USN")
    password: str = Field(..., description="Team password")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    team_leader_usn: Optional[str] = None

class TeamResponse(BaseModel):
    id: int
    team_leader_usn: str
    team_name: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True