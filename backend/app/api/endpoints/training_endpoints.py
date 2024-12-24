from fastapi import APIRouter, HTTPException
from ...core.training_manager import TrainingManager
from ...models.config import TrainingConfig

router = APIRouter()
training_manager = TrainingManager()

@router.post("/start")
async def start_training(config: TrainingConfig):
    try:
        result = await training_manager.start_training(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{training_id}")
async def get_training_status(training_id: str):
    try:
        return training_manager.get_status(training_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))