from typing import List
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

def get_current_team_or_test_team():
    """Get current team or create a test team for LAN testing."""
    if DEBUG:
        # In DEBUG mode, create/use a test team without authentication
        def test_dependency(db: Session = Depends(get_db)):
            # Try to find existing test team
            test_team = db.query(Team).filter(Team.team_leader_usn == "TEST123").first()
            if not test_team:
                # Create test team if it doesn't exist
                test_team = Team(
                    team_leader_usn="TEST123",
                    password_hash="testpass",  # Plain text for testing
                    team_name="Test Team",
                    score=0
                )
                db.add(test_team)
                db.commit()
                db.refresh(test_team)
            return test_team
        return test_dependency
    else:
        return get_current_team

@router.post("/start", response_model=ChallengeStartResponse)
async def start_challenge(
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    """Start a new challenge session for the authenticated team (or test team in DEBUG mode)."""
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
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    """Get current challenge status for the authenticated team."""
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
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    """Update a submission for a specific question."""
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
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    #Verify Active Session
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
    
    # CALL THE STANDALONE RUNNER API with the actual question_id
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8001/run", 
                json={"question_id": question.question_id, "code": payload.code_answer},
                timeout=10.0 # Give it time to run the tests
            )
            judgement = response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Execution Service Down")

    is_correct = (judgement["status"] == "PASS")

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
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    """Upload a .homie file for a specific question."""
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
    db: Session = Depends(get_db),
    current_team: Team = Depends(get_current_team_or_test_team())
):
    """Submit the entire challenge."""
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