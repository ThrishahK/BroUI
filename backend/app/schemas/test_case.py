from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestCaseBase(BaseModel):
    expected_output: str
    is_active: bool = True

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseUpdate(BaseModel):
    expected_output: Optional[str] = None
    is_active: Optional[bool] = None

class TestCaseResponse(TestCaseBase):
    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True
