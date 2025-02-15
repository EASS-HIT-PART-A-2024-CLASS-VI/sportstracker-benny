from pydantic import BaseModel, Field

class ScoreUpdate(BaseModel):
    match_id: int
    team_id: int
    points_scored: int  # 1 for soccer goal, 2 or 3 for basketball...

class ScoreResponse(BaseModel):
    match_id: int = Field(..., alias="id")
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    status: str

    class Config:
        orm_mode = True
