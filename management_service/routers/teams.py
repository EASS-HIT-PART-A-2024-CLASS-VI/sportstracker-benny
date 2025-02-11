# management_service/routers/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter()

@router.post("/", response_model=schemas.TeamResponse)
def create_team(team_data: schemas.TeamCreate, db: Session = Depends(get_db)):
    # Optional: validate that league_id is valid if provided
    if team_data.league_id is not None:
        league = db.query(models.League).get(team_data.league_id)
        if not league:
            raise HTTPException(status_code=400, detail="League does not exist")

    new_team = models.Team(
        name=team_data.name,
        city=team_data.city,
        league_id=team_data.league_id
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.get("/", response_model=list[schemas.TeamResponse])
def list_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()


@router.get("/{team_id}", response_model=schemas.TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=schemas.TeamResponse)
def update_team(
    team_id: int,
    update_data: schemas.TeamUpdate,
    db: Session = Depends(get_db)
):
    team = db.query(models.Team).get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if update_data.name is not None:
        team.name = update_data.name
    if update_data.city is not None:
        team.city = update_data.city
    if update_data.league_id is not None:
        # Validate league if needed
        league = db.query(models.League).get(update_data.league_id)
        if not league:
            raise HTTPException(status_code=400, detail="League does not exist")
        team.league_id = update_data.league_id

    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(team)
    db.commit()
    return
