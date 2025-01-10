from typing import Optional, Dict, List
from pydantic_settings import BaseSettings

from functools import lru_cache
import os

class Settings(BaseSettings):
    # Core API Settings
    PROJECT_NAME: str = "Fine-Tuning Labs"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database Settings
    MONGODB_URL: str = "mongodb://localhost:27017/"
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
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour in seconds
    CACHE_BACKEND: str = "memory"
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "app.log"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # 1 minute
    
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
        
        # Additional environment file for different environments
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            env = os.getenv("ENVIRONMENT", "development")
            return (
                init_settings,
                env_settings,
                file_secret_settings,
                f".env.{env}",
            )

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()

# Create settings instance
settings = get_settings()

# Validation functions
def validate_mongodb_url(url: str) -> bool:
    """Validate MongoDB URL format"""
    # Add validation logic here
    return True

def validate_file_size(size: int) -> bool:
    """Validate file size is within limits"""
    return 0 < size <= settings.MAX_MODEL_SIZE

def get_framework_config(framework: str) -> Dict:
    """Get configuration for specific framework"""
    if framework not in settings.SUPPORTED_FRAMEWORKS:
        raise ValueError(f"Unsupported framework: {framework}")
    return settings.MODEL_CONFIGS[framework]

# Environment-specific configurations
def is_development() -> bool:
    return os.getenv("ENVIRONMENT", "development") == "development"

def is_production() -> bool:
    return os.getenv("ENVIRONMENT", "development") == "production"

# Initialize environment-specific settings
if is_production():
    settings.DEBUG = False
    settings.LOG_LEVEL = "ERROR"
    settings.CORS_ORIGINS = ["https://your-production-domain.com"]
    settings.RATE_LIMIT_REQUESTS = 50