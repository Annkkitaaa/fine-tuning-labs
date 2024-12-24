from fastapi import APIRouter, UploadFile, File, HTTPException
from ...core.model_manager import ModelManager
from ...models.config import ModelConfig

router = APIRouter()
model_manager = ModelManager()

@router.post("/upload")
async def upload_model(file: UploadFile = File(...)):
    try:
        result = await model_manager.upload_model(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_models():
    return {"models": model_manager.list_models()}