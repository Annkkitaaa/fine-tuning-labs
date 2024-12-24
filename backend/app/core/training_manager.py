import asyncio
from typing import Dict, Any
import mlflow
from .fine_tuning import FineTuningManager
from ..models.config import TrainingConfig

class TrainingManager:
    def __init__(self):
        self.fine_tuning_manager = FineTuningManager()
        self.active_trainings: Dict[str, Dict[str, Any]] = {}

    async def start_training(self, config: TrainingConfig) -> dict:
        training_id = str(uuid.uuid4())
        self.active_trainings[training_id] = {
            "status": "pending",
            "config": config,
            "metrics": []
        }
        
        asyncio.create_task(self._run_training(training_id, config))
        return {"training_id": training_id}