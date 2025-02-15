# management_service/schemas.py
#pydantic is used to validate the data thats sent to the DB
# management_service/schemas.py
from pydantic import BaseModel
from typing import Optional, List

# -------------------------
# 1) LEAGUE SCHEMAS
# -------------------------
class LeagueBase(BaseModel):
    name: str
    country: Optional[str] = None

class LeagueCreate(LeagueBase):
    """Schema for creating a new League"""
    pass

class LeagueUpdate(BaseModel):
    """Schema for updating an existing League (fields are optional)"""
    name: Optional[str] = None
    country: Optional[str] = None

class LeagueResponse(LeagueBase):
    """Schema for returning League data"""
    id: int

    class Config:
        orm_mode = True

# -------------------------
# 2) TEAM SCHEMAS
# -------------------------
class TeamBase(BaseModel):
    name: str
    city: str

class TeamCreate(TeamBase):
    """Schema for creating a new Team"""
    league_id: Optional[int] = None  # Might be null if no league

class TeamUpdate(BaseModel):
    """Schema for updating an existing Team"""
    name: Optional[str] = None
    city: Optional[str] = None
    league_id: Optional[int] = None

class TeamResponse(TeamBase):
    id: int
    league_id: Optional[int] = None

    class Config:
        orm_mode = True

# -------------------------
# 3) MATCH SCHEMAS
# -------------------------
class MatchBase(BaseModel):
    league_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    status: Optional[str] = "scheduled"

class MatchCreate(MatchBase):
    """Schema for creating a new Match"""
    pass

class MatchUpdate(BaseModel):
    """Schema for updating an existing Match"""
    league_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    status: Optional[str] = None

class MatchResponse(MatchBase):
    id: int

    class Config:
        orm_mode = True

#---------------------------
#4)USER SCHEMAS
#---------------------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
