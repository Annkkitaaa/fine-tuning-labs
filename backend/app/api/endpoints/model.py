from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Dict, Optional
from pydantic import BaseModel
from ..core.security import get_current_user
import os

router = APIRouter()

class ModelInfo(BaseModel):
    name: str
    framework: str
    params: Optional[Dict] = None

class ModelResponse(BaseModel):
    id: str
    info: ModelInfo
    status: str

@router.post("/upload", response_model=ModelResponse)
async def upload_model(
    file: UploadFile = File(...),
    model_info: ModelInfo = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        file_path = f"models/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "id": file.filename,
            "info": model_info,
            "status": "uploaded"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[ModelResponse])
async def list_models(current_user = Depends(get_current_user)):
    models = []
    for filename in os.listdir("models"):
        models.append({
            "id": filename,
            "info": {
                "name": filename,
                "framework": "auto-detected",
            },
            "status": "available"
        })
    return models