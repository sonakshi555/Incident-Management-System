from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_URL: str
    MONGO_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SIGNAL_QUEUE_SIZE: int = 50000

    class Config:
        env_file = ".env"

settings = Settings()