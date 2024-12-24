import os
import uuid
from fastapi import UploadFile
from ..models.config import ModelConfig
from ..utils.model_utils import save_model_config

class ModelManager:
    def __init__(self):
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)

    async def upload_model(self, file: UploadFile) -> dict:
        model_id = str(uuid.uuid4())
        model_path = os.path.join(self.model_dir, model_id, file.filename)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        with open(model_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {"model_id": model_id, "path": model_path}