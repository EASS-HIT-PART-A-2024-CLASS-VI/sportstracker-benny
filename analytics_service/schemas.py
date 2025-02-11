# analytics_service/schemas.py
from pydantic import BaseModel
from typing import List

class TeamStanding(BaseModel):
    team_id: int
    name: str
    points: int
    wins: int
    draws: int
    losses: int

class StandingsResponse(BaseModel):
    league_id: int
    standings: List[TeamStanding]
