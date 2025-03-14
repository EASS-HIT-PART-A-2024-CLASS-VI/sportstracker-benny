# main.py
from fastapi import FastAPI
from database import engine, Base
from routers import auth, leagues, teams, matches  # the file or package named teams.py
from models import User, Team, League, Match

Base.metadata.drop_all(bind=engine, checkfirst=True)
Base.metadata.create_all(bind=engine)


app = FastAPI()

# This “includes” all endpoints defined in teams, leagues and matches.router
app.include_router(auth.router)
app.include_router(leagues.router, prefix="/leagues", tags=["Leagues"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])