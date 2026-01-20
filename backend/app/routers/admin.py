from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.team import Team
from ..models.question import Question
from ..models.test_case import TestCase
from ..models.challenge_session import ChallengeSession
from ..models.submission import Submission
from ..models.admin import Admin
from ..schemas.team import TeamResponse, TeamCreate
from ..schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionWithTestCases
from ..schemas.test_case import TestCaseCreate, TestCaseUpdate, TestCaseResponse
from ..routers.admin_auth import get_current_admin

router = APIRouter()

# ===== QUESTION MANAGEMENT =====

@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new question."""
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions", response_model=List[QuestionResponse])
async def get_all_questions(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get all questions."""
    questions = db.query(Question).all()
    return questions

@router.get("/questions/{question_id}", response_model=QuestionWithTestCases)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get a specific question with test cases."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update a question."""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a question and all its test cases."""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    return None

# ===== TEST CASE MANAGEMENT =====

@router.post("/questions/{question_id}/testcases", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
async def create_test_case(
    question_id: int,
    test_case: TestCaseCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Add a test case to a question."""
    # Verify question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_test_case = TestCase(question_id=question_id, **test_case.model_dump())
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.get("/questions/{question_id}/testcases", response_model=List[TestCaseResponse])
async def get_test_cases(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get all test cases for a question."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    test_cases = db.query(TestCase).filter(TestCase.question_id == question_id).all()
    return test_cases

@router.put("/testcases/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(
    test_case_id: int,
    test_case_update: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update a test case."""
    db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not db_test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    update_data = test_case_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_test_case, field, value)
    
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.delete("/testcases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a test case."""
    db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not db_test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    db.delete(db_test_case)
    db.commit()
    return None

# ===== TEAM MANAGEMENT =====

@router.get("/teams", response_model=List[TeamResponse])
async def get_all_teams(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get all registered teams."""
    teams = db.query(Team).all()
    return teams

@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new team."""
    import bcrypt
    
    # Check if team already exists
    existing_team = db.query(Team).filter(
        Team.team_leader_usn == team.team_leader_usn.upper()
    ).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team with this USN already exists")

    # Hash the password before storing
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(team.password.encode('utf-8'), salt).decode('utf-8')
    
    # Create new team with hashed password
    team_data = team.model_dump()
    team_data['password'] = hashed_password
    team_data['team_leader_usn'] = team_data['team_leader_usn'].upper()
    
    db_team = Team(**team_data)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a team."""
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    return None

# ===== SESSION MANAGEMENT =====

@router.get("/sessions")
async def get_all_sessions(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get all challenge sessions."""
    sessions = db.query(ChallengeSession).all()
    return sessions

@router.get("/sessions/{session_id}")
async def get_session_results(
    session_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get results for a specific session."""
    session = db.query(ChallengeSession).filter(ChallengeSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    submissions = db.query(Submission).filter(
        Submission.challenge_session_id == session_id
    ).all()

    # Calculate statistics
    saved = sum(1 for s in submissions if s.status.name == "saved")
    flagged = sum(1 for s in submissions if s.status.name == "flagged")
    unattempted = sum(1 for s in submissions if s.status.name == "not_attempted")

    return {
        "session": session,
        "submissions": submissions,
        "statistics": {
            "saved": saved,
            "flagged": flagged,
            "unattempted": unattempted
        }
    }

# ===== CHALLENGE CONTROL =====

@router.post("/challenge/enable")
async def enable_challenge(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Enable the challenge (make it live)."""
    # This could set a global flag in database or config
    return {"message": "Challenge enabled successfully"}

@router.post("/challenge/disable")
async def disable_challenge(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Disable the challenge."""
    # This could set a global flag in database or config
    return {"message": "Challenge disabled successfully"}
