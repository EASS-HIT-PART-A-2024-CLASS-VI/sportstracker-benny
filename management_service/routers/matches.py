# management_service/routers/matches.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.MatchResponse)
def create_match(match_data: schemas.MatchCreate, db: Session = Depends(get_db)):
    # Validate league
    if match_data.league_id is not None:
        league = db.query(models.League).get(match_data.league_id)
        if not league:
            raise HTTPException(status_code=400, detail="League does not exist")

    # Validate home_team, away_team
    if match_data.home_team_id:
        home_team = db.query(models.Team).get(match_data.home_team_id)
        if not home_team:
            raise HTTPException(status_code=400, detail="Home team does not exist")
    if match_data.away_team_id:
        away_team = db.query(models.Team).get(match_data.away_team_id)
        if not away_team:
            raise HTTPException(status_code=400, detail="Away team does not exist")

    new_match = models.Match(
        league_id=match_data.league_id,
        home_team_id=match_data.home_team_id,
        away_team_id=match_data.away_team_id,
        status=match_data.status
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match


@router.get("/", response_model=list[schemas.MatchResponse])
def list_matches(db: Session = Depends(get_db)):
    return db.query(models.Match).all()


@router.get("/{match_id}", response_model=schemas.MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/{match_id}", response_model=schemas.MatchResponse)
def update_match(match_id: int, update_data: schemas.MatchUpdate, db: Session = Depends(get_db)):
    match = db.query(models.Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if update_data.league_id is not None:
        league = db.query(models.League).get(update_data.league_id)
        if not league:
            raise HTTPException(status_code=400, detail="League does not exist")
        match.league_id = update_data.league_id

    if update_data.home_team_id is not None:
        home_team = db.query(models.Team).get(update_data.home_team_id)
        if not home_team:
            raise HTTPException(status_code=400, detail="Home team does not exist")
        match.home_team_id = update_data.home_team_id

    if update_data.away_team_id is not None:
        away_team = db.query(models.Team).get(update_data.away_team_id)
        if not away_team:
            raise HTTPException(status_code=400, detail="Away team does not exist")
        match.away_team_id = update_data.away_team_id

    if update_data.status is not None:
        match.status = update_data.status

    db.commit()
    db.refresh(match)
    return match


@router.delete("/{match_id}", status_code=204)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    db.delete(match)
    db.commit()
    return
