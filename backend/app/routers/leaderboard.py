from typing import List, Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.team import Team
from ..models.challenge_session import ChallengeSession
from ..models.submission import Submission
from ..models.question import Question

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])

@router.get("/", response_model=List[dict])
def get_leaderboard(request: Request, db: Session = Depends(get_db)):
    """
    Simple leaderboard:
    - Uses the latest challenge session per team (highest session id).
    - Score = sum(question.points) for correct submissions in that session.
    """
    # Security Check: Only allow requests from the server machine (localhost)
    if request.client.host not in ("127.0.0.1", "localhost", "::1"):
        raise HTTPException(
            status_code=403, 
            detail="Access Denied: The leaderboard is only viewable from the server laptop."
        )

    teams = db.query(Team).filter(Team.is_active == True).all()
    if not teams:
        return []

    leaderboard_rows = []

    for team in teams:
        latest_session: Optional[ChallengeSession] = (
            db.query(ChallengeSession)
            .filter(ChallengeSession.team_id == team.id)
            .order_by(ChallengeSession.id.desc())
            .first()
        )

        if not latest_session:
            leaderboard_rows.append(
                {
                    "team_id": team.id,
                    "team_name": team.team_name,
                    "team_leader_usn": team.team_leader_usn,
                    "session_id": None,
                    "score": 0,
                    "solved": 0,
                }
            )
            continue

        correct_submissions = (
            db.query(Submission, Question)
            .join(Question, Question.id == Submission.question_id)
            .filter(Submission.challenge_session_id == latest_session.id)
            .filter(Submission.is_correct == True)
            .all()
        )

        score = sum(q.points for _, q in correct_submissions)
        solved = len(correct_submissions)

        leaderboard_rows.append(
            {
                "team_id": team.id,
                "team_name": team.team_name,
                "team_leader_usn": team.team_leader_usn,
                "session_id": latest_session.id,
                "score": score,
                "solved": solved,
            }
        )

    # Sort by score desc, solved desc, then team id asc for stable ordering
    leaderboard_rows.sort(key=lambda r: (-r["score"], -r["solved"], r["team_id"]))

    for idx, row in enumerate(leaderboard_rows, start=1):
        row["rank"] = idx

    return leaderboard_rows
