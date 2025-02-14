from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/sportsdb"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate a global settings object:
settings = Settings()
