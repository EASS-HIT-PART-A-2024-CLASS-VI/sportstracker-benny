# management_service/routers/leagues.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.LeagueResponse)
def create_league(
    league_data: schemas.LeagueCreate,
    db: Session = Depends(get_db)
):
    new_league = models.League(
        name=league_data.name,
        country=league_data.country
    )
    db.add(new_league)
    db.commit()
    db.refresh(new_league)
    return new_league


@router.get("/", response_model=list[schemas.LeagueResponse])
def list_leagues(db: Session = Depends(get_db)):
    leagues = db.query(models.League).all()
    return leagues


@router.get("/{league_id}", response_model=schemas.LeagueResponse)
def get_league(league_id: int, db: Session = Depends(get_db)):
    league = db.query(models.League).get(league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@router.put("/{league_id}", response_model=schemas.LeagueResponse)
def update_league(
    league_id: int,
    update_data: schemas.LeagueUpdate,
    db: Session = Depends(get_db)
):
    league = db.query(models.League).get(league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    if update_data.name is not None:
        league.name = update_data.name
    if update_data.country is not None:
        league.country = update_data.country

    db.commit()
    db.refresh(league)
    return league


@router.delete("/{league_id}", status_code=204)
def delete_league(league_id: int, db: Session = Depends(get_db)):
    league = db.query(models.League).get(league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    db.delete(league)
    db.commit()
    return
