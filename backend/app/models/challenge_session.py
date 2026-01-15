from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class ChallengeSession(Base):
    __tablename__ = "challenge_sessions"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    total_questions = Column(Integer, default=30)
    time_remaining_seconds = Column(Integer, default=10800)  # 3 hours in seconds

    # Relationship
    team = relationship("Team")

    # Submissions will be linked through Submission model