from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    question_id: int
    code_answer: Optional[str] = None
    status: str = "not_attempted"  # not_attempted, saved, flagged, submitted

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionUpdate(BaseModel):
    code_answer: Optional[str] = None
    status: Optional[str] = None

class SubmissionResponse(SubmissionBase):
    id: int
    challenge_session_id: int
    file_path: Optional[str] = None
    submitted_at: datetime

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