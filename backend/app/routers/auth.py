from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.team import Team
from ..schemas.auth import TeamLogin, Token, TokenData, TeamResponse
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    # Try bcrypt first, then fallback to SHA256 for testing
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback to SHA256 for test accounts (accept exact or uppercased input)
        import hashlib
        if hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password:
            return True
        return hashlib.sha256(plain_password.upper().encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def authenticate_team(db: Session, team_leader_usn: str, password: str) -> Optional[Team]:
    """Authenticate a team with USN and password."""
    team = db.query(Team).filter(Team.team_leader_usn == team_leader_usn.upper()).first()
    if not team:
        return None
    if not verify_password(password, team.password):
        return None
    return team

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_team(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Team:
    """Get current authenticated team from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        team_leader_usn: str = payload.get("sub")
        if team_leader_usn is None:
            raise credentials_exception
        token_data = TokenData(team_leader_usn=team_leader_usn)
    except JWTError:
        raise credentials_exception

    team = db.query(Team).filter(Team.team_leader_usn == token_data.team_leader_usn).first()
    if team is None:
        raise credentials_exception
    return team

@router.post("/login", response_model=Token)
async def login_for_access_token(
    team_credentials: TeamLogin,
    db: Session = Depends(get_db)
):
    """Login endpoint for teams."""
    try:
        team = authenticate_team(
            db,
            team_leader_usn=team_credentials.team_leader_usn,
            password=team_credentials.password
        )
        if not team:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect USN or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": team.team_leader_usn}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/me", response_model=TeamResponse)
async def read_teams_me(current_team: Team = Depends(get_current_team)):
    """Get current authenticated team's information."""
    return current_team

@router.post("/register")
async def register_team(
    team_leader_usn: str,
    password: str,
    team_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Register a new team (admin functionality)."""
    # Check if team already exists
    existing_team = db.query(Team).filter(Team.team_leader_usn == team_leader_usn.upper()).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team with this USN already exists")

    # Create new team
    hashed_password = get_password_hash(password)
    new_team = Team(
        team_leader_usn=team_leader_usn.upper(),
        password=hashed_password,
        team_name=team_name
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return {"message": "Team registered successfully", "team_id": new_team.id}