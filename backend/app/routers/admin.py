from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.team import Team
from ..models.challenge_session import ChallengeSession
from ..models.submission import Submission
from ..schemas.team import TeamResponse, TeamCreate
from ..routers.auth import get_current_team

router = APIRouter()

# TODO: Add proper admin authentication (for now using team auth)

@router.get("/teams", response_model=List[TeamResponse])
async def get_all_teams(
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
):
    """Get all registered teams."""
    teams = db.query(Team).all()
    return teams

@router.post("/teams", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
):
    """Create a new team."""
    # Check if team already exists
    existing_team = db.query(Team).filter(
        Team.team_leader_usn == team.team_leader_usn.upper()
    ).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team with this USN already exists")

    # Create new team
    db_team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/sessions")
async def get_all_sessions(
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
):
    """Get all challenge sessions."""
    sessions = db.query(ChallengeSession).all()
    return sessions

@router.get("/results/{session_id}")
async def get_session_results(
    session_id: int,
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
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

@router.post("/challenge/enable")
async def enable_challenge(
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
):
    """Enable the challenge (make it live)."""
    # This could set a global flag in database or config
    return {"message": "Challenge enabled successfully"}

@router.post("/challenge/disable")
async def disable_challenge(
    db: Session = Depends(get_db),
    current_team = Depends(get_current_team)  # TODO: Admin check
):
    """Disable the challenge."""
    # This could set a global flag in database or config
    return {"message": "Challenge disabled successfully"}