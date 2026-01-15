from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class SubmissionStatus(enum.Enum):
    not_attempted = "not_attempted"
    saved = "saved"
    flagged = "flagged"
    submitted = "submitted"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    challenge_session_id = Column(Integer, ForeignKey("challenge_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    code_answer = Column(Text)  # Code written in textarea
    file_path = Column(String)  # Path to uploaded .homie file
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.not_attempted)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Execution / judging fields
    attempts = Column(Integer, default=0, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)  # locked after correct
    last_result = Column(Integer, nullable=True)  # 1 correct, 0 wrong (from Execute API)
    last_executed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    challenge_session = relationship("ChallengeSession")
    question = relationship("Question")