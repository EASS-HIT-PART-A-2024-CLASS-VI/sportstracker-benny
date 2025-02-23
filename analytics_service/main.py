# analytics_service/main.py
import time
import sys
import psycopg2
from fastapi import FastAPI
from config import settings
import database
from database import Base, engine
import routers
from routers import analytics

# Retry logic to wait for DB
max_retries = 5
retry_wait_sec = 5

for attempt in range(1, max_retries + 1):
    try:
        # Attempt a direct connection using psycopg2
        conn = psycopg2.connect(settings.DATABASE_URL, connect_timeout=3)
        conn.close()
        print("Database connection successful!")
        break
    except psycopg2.OperationalError as e:
        print(f"[Attempt {attempt}/{max_retries}] DB not ready: {e}")
        if attempt == max_retries:
            print("Maximum retries reached. Exiting.")
            sys.exit(1)  # Or raise an exception
        print(f"Waiting {retry_wait_sec} seconds before retrying...")
        time.sleep(retry_wait_sec)

Base.metadata.drop_all(bind=engine, checkfirst=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analytics Service")

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
