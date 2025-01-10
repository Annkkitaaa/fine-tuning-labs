from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Fine-Tuning Labs",
    description="A comprehensive platform for fine-tuning machine learning models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database configuration (MongoDB)
MONGODB_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "fine-tuning-labs")

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Add your token verification logic here
        return {"username": "test_user"}  # Replace with actual user data
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Fine-Tuning Labs API",
        "docs_url": "/docs",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }

# Protected endpoint example
@app.get("/user/me")
async def read_user_me(current_user: dict = Depends(get_current_user)):
    return current_user

# Import routers
from app.api.endpoints import models, training, metrics

# Include routers with prefixes
app.include_router(
    models.router,
    prefix="/api/v1/models",
    tags=["Models"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    training.router,
    prefix="/api/v1/training",
    tags=["Training"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["Metrics"],
    dependencies=[Depends(get_current_user)]
)

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "detail": "Internal server error",
        "status_code": 500
    }

# Configuration endpoints
@app.get("/api/v1/config")
async def get_config(current_user: dict = Depends(get_current_user)):
    return {
        "supported_frameworks": ["pytorch", "tensorflow", "scikit-learn"],
        "available_models": {
            "pytorch": ["bert-base", "roberta-base"],
            "tensorflow": ["bert-base-tf", "distilbert-tf"],
            "scikit-learn": ["random-forest", "svm"]
        },
        "max_training_time": 3600,  # in seconds
        "max_file_size": 100 * 1024 * 1024  # 100MB
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    # Add any startup initialization here
    print("Starting Fine-Tuning Labs API...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    # Add cleanup code here
    print("Shutting down Fine-Tuning Labs API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)