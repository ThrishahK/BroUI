from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String, unique=True, index=True, nullable=False)  # E01, M04, H10, etc.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    sample_input = Column(Text)
    sample_output = Column(Text)
    reference_solution = Column(Text)  # Reference brocode solution from .homie files
    difficulty = Column(String, default="medium")  # easy, medium, hard
    points = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    test_cases = relationship("TestCase", back_populates="question", cascade="all, delete-orphan")