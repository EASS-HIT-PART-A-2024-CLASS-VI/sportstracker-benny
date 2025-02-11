# management_service/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
#DB Models
class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # More fields here...

    # Relationship if you want to link to teams or matches
    teams = relationship("Team", back_populates="league")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    league = relationship("League", back_populates="teams")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    status = Column(String, default="scheduled")
    # start_time = Column(DateTime)
