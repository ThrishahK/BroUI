from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.question import Question
from ..schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse, QuestionPublic
)
from ..routers.auth import get_current_team  # For admin authentication

router = APIRouter()

@router.get("/", response_model=List[QuestionResponse])
async def get_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # Admin only
):
    """Get all questions (admin endpoint)."""
    questions = db.query(Question).offset(skip).limit(limit).all()
    return questions

@router.post("/", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # Admin only
):
    """Create a new question (admin endpoint)."""
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # Admin only
):
    """Get a specific question (admin endpoint)."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # Admin only
):
    """Update a question (admin endpoint)."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    update_data = question_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question

@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # Admin only
):
    """Delete a question (admin endpoint)."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}

# Public endpoints for challenge participants
@router.get("/public/all", response_model=List[QuestionPublic])
async def get_public_questions(db: Session = Depends(get_db)):
    """Get all active questions for challenge participants."""
    questions = db.query(Question).filter(Question.is_active == True).all()
    return questions

@router.get("/public/{question_id}", response_model=QuestionPublic)
async def get_public_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific active question for challenge participants."""
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.is_active == True
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question