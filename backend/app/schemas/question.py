from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class QuestionBase(BaseModel):
    question_id: str  # E01, M04, H10, etc.
    title: str
    description: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str = "medium"
    points: int = 10

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_id: Optional[str] = None
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
    question_id: str  # E01, M04, H10, etc.
    title: str
    description: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str
    points: int

    class Config:
        from_attributes = True

class QuestionWithTestCases(QuestionResponse):
    """Question with test cases for admin."""
    test_cases: List["TestCaseResponse"] = []

# Import for forward reference
from .test_case import TestCaseResponse
QuestionWithTestCases.model_rebuild()