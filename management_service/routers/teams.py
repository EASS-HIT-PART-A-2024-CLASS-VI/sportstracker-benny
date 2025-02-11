# management_service/routers/teams.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.TeamResponse)
def create_team(team_data: schemas.TeamCreate, db: Session = Depends(get_db)):
    new_team = models.Team(name=team_data.name, city=team_data.city)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team