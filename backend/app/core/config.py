from typing import Optional, Dict, List
from pydantic import BaseSettings, validator
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Core API Settings
    PROJECT_NAME: str = "Fine-Tuning Labs"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security Settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database Settings
    MONGO_USER: str
    MONGO_PASS: str
    DATABASE_URL: str
    DATABASE_NAME: str = "fine_tuning_labs"
    
    # Model Storage Settings
    MODEL_STORAGE_PATH: str = "models/"
    MAX_MODEL_SIZE: int = 1000 * 1024 * 1024  # 1000MB
    ALLOWED_MODEL_EXTENSIONS: List[str] = [".pt", ".pth", ".h5", ".keras", ".pkl", ".joblib"]
    
    # Training Settings
    MAX_TRAINING_JOBS: int = 5
    DEFAULT_BATCH_SIZE: int = 32
    DEFAULT_EPOCHS: int = 10
    MAX_TRAINING_TIME: int = 3600  # 1 hour in seconds
    
    # ML Framework Settings
    SUPPORTED_FRAMEWORKS: List[str] = ["pytorch", "tensorflow", "scikit-learn"]
    DEFAULT_FRAMEWORK: str = "pytorch"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://fine-tuning-labs.vercel.app"  # Add your Vercel domain
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Model Configurations
    MODEL_CONFIGS: Dict[str, Dict] = {
        "pytorch": {
            "supported_models": ["bert-base", "roberta-base"],
            "max_sequence_length": 512,
        },
        "tensorflow": {
            "supported_models": ["bert-base-tf", "distilbert-tf"],
            "max_sequence_length": 512,
        },
        "scikit-learn": {
            "supported_models": ["random-forest", "svm"],
            "max_features": 1000,
        }
    }

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v: Optional[str], values: Dict) -> str:
        if not v:
            user = values.get("MONGO_USER")
            password = values.get("MONGO_PASS")
            if user and password:
                return f"mongodb+srv://{user}:{password}@cluster0.mongodb.net/fine-tuning-labs?retryWrites=true&w=majority"
        return v

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Create settings instance
settings = get_settings()

# Environment-specific configurations
def is_development() -> bool:
    return os.getenv("ENVIRONMENT", "development") == "development"

def is_production() -> bool:
    return os.getenv("ENVIRONMENT", "development") == "production"

# Initialize environment-specific settings
if is_production():
    settings.DEBUG = False
    settings.CORS_ORIGINS.append("https://fine-tuning-labs.vercel.app")  # Add your Vercel domain