from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import httpx
from test_runner import test_submission

from ..database import get_db
from ..models.team import Team
from ..models.question import Question
from ..models.challenge_session import ChallengeSession
from ..models.submission import Submission, SubmissionStatus
from ..schemas.challenge import (
    ChallengeStartResponse, ChallengeStatusResponse,
    ChallengeSubmitRequest, ChallengeSubmitResponse,
    SubmissionUpdate, ExecuteRequest, ExecuteResponse
)
from ..routers.auth import get_current_team
from ..config import (
    CHALLENGE_DURATION_MINUTES,
    DEBUG,
    UPLOAD_DIR,
    ALLOWED_EXTENSIONS,
    MAX_QUESTIONS,
    EXECUTE_API_BASE_URL,
    EXECUTE_API_TOKEN,
    EXECUTE_API_TIMEOUT_SECONDS,
)
from ..services.judge_service import judge_service

router = APIRouter()

def get_active_challenge_session(team_id: int, db: Session) -> ChallengeSession:
    """Get active challenge session for a team."""
    return db.query(ChallengeSession).filter(
        ChallengeSession.team_id == team_id,
        ChallengeSession.is_active == True
    ).first()

def create_submissions_for_session(session_id: int, db: Session):
    """Create submission records for all questions in a session."""
    questions = db.query(Question).filter(Question.is_active == True).limit(MAX_QUESTIONS).all()

    for question in questions:
        submission = Submission(
            challenge_session_id=session_id,
            question_id=question.id,
            status=SubmissionStatus.not_attempted
        )
        db.add(submission)

    db.commit()

from fastapi.security import OAuth2PasswordBearer
from ..routers.auth import get_current_team, oauth2_scheme

# Optional scheme for DEBUG mode fallback
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_team_for_challenge(db: Session, token: Optional[str] = None):
    """
    Get current team for challenge endpoints, with DEBUG fallback.

    This function takes the database session as a parameter to avoid
    creating multiple sessions and transaction issues.
    """
    # 1. Try to authenticate with the token if provided
    if token:
        try:
            from ..routers.auth import SECRET_KEY, ALGORITHM
            from jose import jwt

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            team_leader_usn: str = payload.get("sub")
            if team_leader_usn:
                team = db.query(Team).filter(Team.team_leader_usn == team_leader_usn).first()
                if team:
                    return team
        except Exception:
            # Token invalid/expired - fall through to debug check
            pass

    # 2. Fallback for DEBUG mode
    if DEBUG:
        print("\n[DEBUG] Using Fallback 'Test Team' for challenge endpoint")

        # Create/Get Test Team
        test_team = db.query(Team).filter(Team.team_leader_usn == "TEST123").first()
        if not test_team:
            test_team = Team(
                team_leader_usn="TEST123",
                password_hash="testpass",
                team_name="Test Team",
                score=0
            )
            db.add(test_team)
            db.commit()
            db.refresh(test_team)
        return test_team

    # 3. No token and not in DEBUG mode -> Error
    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/start", response_model=ChallengeStartResponse)
async def start_challenge(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    """Start a new challenge session for the authenticated team (or test team in DEBUG mode)."""
    current_team = get_current_team_for_challenge(db, token)

    # Check if team already has an active session
    existing_session = get_active_challenge_session(current_team.id, db)
    if existing_session:
        raise HTTPException(
            status_code=400,
            detail="Team already has an active challenge session"
        )

    # Create new challenge session
    session = ChallengeSession(
        team_id=current_team.id,
        time_remaining_seconds=CHALLENGE_DURATION_MINUTES * 60
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    # Create submissions for all questions
    create_submissions_for_session(session.id, db)

    # Get questions for response
    questions = db.query(Question).filter(Question.is_active == True).limit(MAX_QUESTIONS).all()
    question_data = [
        {
            "id": q.id,
            "title": q.title,
            "difficulty": q.difficulty,
            "points": q.points
        } for q in questions
    ]

    return {
        "session": session,
        "questions": question_data
    }

@router.get("/status", response_model=ChallengeStatusResponse)
async def get_challenge_status(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    """Get current challenge status for the authenticated team."""
    current_team = get_current_team_for_challenge(db, token)
    session = get_active_challenge_session(current_team.id, db)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="No active challenge session found"
        )

    # Update time remaining
    if session.started_at:
        elapsed = datetime.utcnow() - session.started_at.replace(tzinfo=None)
        remaining = max(0, session.time_remaining_seconds - int(elapsed.total_seconds()))
        session.time_remaining_seconds = remaining

        # Auto-end session if time is up
        if remaining <= 0:
            session.is_active = False
            session.ended_at = datetime.utcnow()
            db.commit()

    submissions = db.query(Submission).filter(
        Submission.challenge_session_id == session.id
    ).all()

    return {
        "session": session,
        "submissions": submissions,
        "time_remaining_seconds": session.time_remaining_seconds
    }

@router.put("/submission/{question_id}")
async def update_submission(
    question_id: int,
    submission_update: SubmissionUpdate,
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    """Update a submission for a specific question."""
    current_team = get_current_team_for_challenge(db, token)
    session = get_active_challenge_session(current_team.id, db)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="No active challenge session found"
        )

    submission = db.query(Submission).filter(
        Submission.challenge_session_id == session.id,
        Submission.question_id == question_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Update submission data
    update_data = submission_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status":
            submission.status = SubmissionStatus(value)
        else:
            setattr(submission, field, value)

    submission.submitted_at = datetime.utcnow()
    db.commit()
    db.refresh(submission)

    return {"message": "Submission updated successfully"}


# @router.post("/execute/{question_id}", response_model=ExecuteResponse)
@router.post("/execute/{question_id}", response_model=ExecuteResponse)
async def execute_submission(
    question_id: int,
    payload: ExecuteRequest,
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    #Verify Active Session
    current_team = get_current_team_for_challenge(db, token)
    session = get_active_challenge_session(current_team.id, db)
    if not session:
        raise HTTPException(status_code=404, detail="No active challenge session found")

    #Get/Create Submission Record
    submission = db.query(Submission).filter(
        Submission.challenge_session_id == session.id,
        Submission.question_id == question_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission record not found")

    
    # Check max attempts
    MAX_ATTEMPTS = 5
    if (submission.attempts or 0) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=400, 
            detail=f"Max execution attempts ({MAX_ATTEMPTS}) reached for this question."
        )

    if submission.is_locked:
        return {
            "question_id": question_id,
            "result": submission.last_result,
            "attempts": submission.attempts,
            "is_correct": submission.is_correct,
            "is_locked": True
        }

    # Fetch the question to get its question_id (E01, M04, H10, etc.)
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # For LAN testing, use the test_runner directly instead of external judge service
    if DEBUG:
        # Use the test_runner module directly
        try:
            from test_runner import test_submission
            result = test_submission(question.question_id, payload.code_answer)
            is_correct = (result["status"] == "PASS")
        except Exception as e:
            print(f"Test runner error: {e}")
            raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
    else:
        # Use external judge service for production
        try:
            from ..services.judge_service import judge_service
            result = await judge_service.judge_submission(question.question_id, payload.code_answer)
            is_correct = (result == 1)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Judge service error: {str(e)}")

    #Update Database
    submission.code_answer = payload.code_answer
    submission.attempts = (submission.attempts or 0) + 1
    submission.last_result = 1 if is_correct else 0
    submission.is_correct = is_correct
    submission.is_locked = is_correct # Lock if fully correct
    submission.last_executed_at = datetime.utcnow()
    
    if is_correct:
        submission.status = "submitted"

    db.commit()
    db.refresh(submission)

    return {
        "question_id": question_id,
        "result": submission.last_result,
        "attempts": submission.attempts,
        "is_correct": submission.is_correct,
        "is_locked": submission.is_locked,
    }

@router.post("/upload/{question_id}")
async def upload_file(
    question_id: int,
    file: UploadFile = File(...),
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    """Upload a .homie file for a specific question."""
    current_team = get_current_team_for_challenge(db, token)
    session = get_active_challenge_session(current_team.id, db)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="No active challenge session found"
        )

    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only .homie files are allowed"
        )

    # Create unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_team.team_leader_usn}_{question_id}_{timestamp}.homie"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Update submission with file path
    submission = db.query(Submission).filter(
        Submission.challenge_session_id == session.id,
        Submission.question_id == question_id
    ).first()

    if submission:
        submission.file_path = file_path
        submission.submitted_at = datetime.utcnow()
        db.commit()

    return {"message": "File uploaded successfully", "file_path": file_path}

@router.post("/submit", response_model=ChallengeSubmitResponse)
async def submit_challenge(
    submit_data: ChallengeSubmitRequest,
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    """Submit the entire challenge."""
    current_team = get_current_team_for_challenge(db, token)
    session = get_active_challenge_session(current_team.id, db)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="No active challenge session found"
        )

    # Update all submissions
    for submission_update in submit_data.submissions:
        submission = db.query(Submission).filter(
            Submission.challenge_session_id == session.id,
            Submission.question_id == submission_update.question_id
        ).first()

        if submission:
            update_data = submission_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if field == "status":
                    submission.status = SubmissionStatus(value)
                else:
                    setattr(submission, field, value)
            submission.submitted_at = datetime.utcnow()

    # End the session
    session.is_active = False
    session.ended_at = datetime.utcnow()
    db.commit()

    # Calculate statistics
    submissions = db.query(Submission).filter(
        Submission.challenge_session_id == session.id
    ).all()

    saved = sum(1 for s in submissions if s.status == SubmissionStatus.saved)
    flagged = sum(1 for s in submissions if s.status == SubmissionStatus.flagged)
    unattempted = sum(1 for s in submissions if s.status == SubmissionStatus.not_attempted)

    return {
        "message": "Challenge submitted successfully",
        "total_saved": saved,
        "total_flagged": flagged,
        "total_unattempted": unattempted
    }