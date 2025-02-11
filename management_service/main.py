# main.py
from fastapi import FastAPI
from routers import leagues, teams, matches  # the file or package named teams.py

app = FastAPI()

# This “includes” all endpoints defined in teams, leagues and matches.router
app.include_router(leagues.router, prefix="/leagues", tags=["Leagues"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])