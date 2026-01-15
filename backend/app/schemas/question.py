from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    title: str
    description: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str = "medium"
    points: int = 10

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: Optional[str] = None
    points: Optional[int] = None
    is_active: Optional[bool] = None

class QuestionResponse(QuestionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class QuestionPublic(BaseModel):
    """Public question data for challenge participants."""
    id: int
    title: str
    description: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str
    points: int

    class Config:
        from_attributes = True