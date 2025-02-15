from fastapi import FastAPI
from routers import scores
app = FastAPI()

app.include_router(scores.router, prefix="/score")
