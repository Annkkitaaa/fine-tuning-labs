from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fine-Tuning Labs"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017/"
    DATABASE_NAME: str = "fine_tuning_labs"
    
    # Model Storage
    MODEL_STORAGE_PATH: str = "models/"
    MAX_MODEL_SIZE: int = 1000 * 1024 * 1024  # 1000MB
    
    # Training
    MAX_TRAINING_JOBS: int = 5
    DEFAULT_BATCH_SIZE: int = 32
    DEFAULT_EPOCHS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()