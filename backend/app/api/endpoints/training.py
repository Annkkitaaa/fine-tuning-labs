from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from app.core.security import get_current_user
from app.ml.training.hyperparameter import HyperparameterTuner
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models
class TrainingConfig(BaseModel):
    model_id: str
    dataset_path: str
    hyperparameters: Dict[str, Any]
    framework: Optional[str] = None

class TrainingJob(BaseModel):
    job_id: str
    status: str
    progress: float
    metrics: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None

class TrainingResponse(BaseModel):
    job_id: str
    status: str
    message: str

# Storage for active training jobs
active_jobs: Dict[str, TrainingJob] = {}

# Training Status Enum
TRAINING_STATUS = {
    "INITIALIZED": "initialized",
    "RUNNING": "running",
    "COMPLETED": "completed",
    "FAILED": "failed"
}

def train_model_task(job_id: str, config: TrainingConfig):
    """
    Background task for model training
    """
    try:
        logger.info(f"Starting training job {job_id}")
        active_jobs[job_id].status = TRAINING_STATUS["RUNNING"]
        
        # Initialize tuner
        tuner = HyperparameterTuner(model=None, dataset=None)
        
        # Simulate training progress
        total_steps = 10
        for i in range(total_steps):
            if job_id not in active_jobs:
                logger.warning(f"Job {job_id} was cancelled")
                return
                
            time.sleep(1)  # Simulate work
            progress = (i + 1) / total_steps
            active_jobs[job_id].progress = progress
            logger.info(f"Job {job_id} progress: {progress:.2%}")
        
        # Update job with completion status and metrics
        active_jobs[job_id].status = TRAINING_STATUS["COMPLETED"]
        active_jobs[job_id].metrics = {
            "accuracy": 0.95,
            "loss": 0.05,
            "validation_accuracy": 0.93,
            "validation_loss": 0.07
        }
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Training failed for job {job_id}: {error_msg}")
        active_jobs[job_id].status = TRAINING_STATUS["FAILED"]
        active_jobs[job_id].error_message = error_msg

@router.post("/start", response_model=TrainingResponse)
async def start_training(
    config: TrainingConfig,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new training job
    """
    try:
        job_id = f"job_{len(active_jobs) + 1}"
        
        # Create new job
        job = TrainingJob(
            job_id=job_id,
            status=TRAINING_STATUS["INITIALIZED"],
            progress=0.0
        )
        active_jobs[job_id] = job
        
        # Add training task to background tasks
        background_tasks.add_task(train_model_task, job_id, config)
        
        return TrainingResponse(
            job_id=job_id,
            status=TRAINING_STATUS["INITIALIZED"],
            message="Training job started successfully"
        )
        
    except Exception as e:
        logger.error(f"Error starting training: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start training: {str(e)}"
        )

@router.get("/status/{job_id}", response_model=TrainingJob)
async def get_training_status(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get the status of a training job
    """
    if job_id not in active_jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    return active_jobs[job_id]

@router.get("/list", response_model=List[TrainingJob])
async def list_training_jobs(current_user: dict = Depends(get_current_user)):
    """
    List all training jobs
    """
    return list(active_jobs.values())

@router.delete("/cancel/{job_id}", response_model=TrainingResponse)
async def cancel_training(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel a training job
    """
    if job_id not in active_jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    
    job = active_jobs[job_id]
    if job.status in [TRAINING_STATUS["COMPLETED"], TRAINING_STATUS["FAILED"]]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel job in {job.status} status"
        )
    
    # Remove job from active jobs
    del active_jobs[job_id]
    
    return TrainingResponse(
        job_id=job_id,
        status="cancelled",
        message="Training job cancelled successfully"
    )

@router.get("/metrics/{job_id}")
async def get_training_metrics(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed metrics for a training job
    """
    if job_id not in active_jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    
    job = active_jobs[job_id]
    if not job.metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No metrics available for job {job_id}"
        )
    
    return job.metrics