# main.py
from fastapi import FastAPI
from routers import teams  # the file or package named teams.py

app = FastAPI()

# This “includes” all endpoints defined in teams.router
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
