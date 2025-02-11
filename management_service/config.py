from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    # Optionally specify a .env file if you want to store
    # environment variables there instead of docker-compose.
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate a global settings object:
settings = Settings()
