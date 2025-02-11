from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Match
from schemas import ScoreUpdate, ScoreResponse

router = APIRouter()

@router.post("/update", response_model=ScoreResponse)
def post_score_update(score: ScoreUpdate, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == score.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Determine if the scoring team is home or away
    if match.home_team_id == score.team_id:
        match.home_score += score.points_scored
    elif match.away_team_id == score.team_id:
        match.away_score += score.points_scored
    else:
        raise HTTPException(status_code=400, detail="Team not in this match")

    # Possibly set match.status to "in_progress" if it was "scheduled"
    if match.status == "scheduled":
        match.status = "in_progress"

    db.commit()
    db.refresh(match)
    return match

@router.get("/{match_id}", response_model=ScoreResponse)
def get_live_score(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
