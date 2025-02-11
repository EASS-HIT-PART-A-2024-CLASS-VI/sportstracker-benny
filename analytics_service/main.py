# analytics_service/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import analytics

# Optionally create tables if not using Alembic migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analytics Service")

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
