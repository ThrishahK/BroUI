from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    question_id: int
    code_answer: Optional[str] = None
    status: str = "not_attempted"  # not_attempted, saved, flagged, submitted
    attempts: int = 0
    is_correct: bool = False
    is_locked: bool = False
    last_result: Optional[int] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionUpdate(BaseModel):
    code_answer: Optional[str] = None
    status: Optional[str] = None

class ExecuteRequest(BaseModel):
    code_answer: str

class ExecuteResponse(BaseModel):
    question_id: int
    result: int  # 1 correct, 0 wrong
    attempts: int
    is_correct: bool
    is_locked: bool

class SubmissionResponse(SubmissionBase):
    id: int
    challenge_session_id: int
    file_path: Optional[str] = None
    submitted_at: datetime
    last_executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChallengeSessionResponse(BaseModel):
    id: int
    team_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_active: bool
    total_questions: int
    time_remaining_seconds: int

    class Config:
        from_attributes = True

class ChallengeStartResponse(BaseModel):
    session: ChallengeSessionResponse
    questions: List[dict]  # Simplified question data

class ChallengeStatusResponse(BaseModel):
    session: ChallengeSessionResponse
    submissions: List[SubmissionResponse]
    time_remaining_seconds: int

class ChallengeSubmitRequest(BaseModel):
    submissions: List[SubmissionUpdate]

class ChallengeSubmitResponse(BaseModel):
    message: str
    total_saved: int
    total_flagged: int
    total_unattempted: int