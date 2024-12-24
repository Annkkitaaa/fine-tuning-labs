from pydantic import BaseModel
from typing import Dict, Any, Optional

class ModelConfig(BaseModel):
    framework: str
    name: str
    description: Optional[str] = None

class TrainingConfig(BaseModel):
    model_id: str
    framework: str
    hyperparameters: Dict[str, Any]
    epochs: int = 10
    batch_size: int = 32