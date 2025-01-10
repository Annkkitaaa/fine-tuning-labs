from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from app.core.security import get_current_user
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models
class ModelInfo(BaseModel):
    name: str
    framework: str
    params: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    version: Optional[str] = None

class ModelResponse(BaseModel):
    id: str
    info: ModelInfo
    status: str
    created_at: str
    last_modified: Optional[str] = None
    size: Optional[int] = None

class ModelUpdateRequest(BaseModel):
    info: Optional[ModelInfo] = None
    status: Optional[str] = None

# Constants
ALLOWED_FRAMEWORKS = ["pytorch", "tensorflow", "scikit-learn"]
ALLOWED_EXTENSIONS = [".pt", ".pth", ".h5", ".keras", ".pkl", ".joblib"]
MODEL_STORAGE_PATH = "models"

# Ensure model storage directory exists
os.makedirs(MODEL_STORAGE_PATH, exist_ok=True)

def validate_model_file(filename: str) -> bool:
    """Validate model file extension"""
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)

@router.post("/upload", response_model=ModelResponse)
async def upload_model(
    file: UploadFile = File(...),
    model_info: ModelInfo = Depends(),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a new model file with metadata
    """
    try:
        # Validate framework
        if model_info.framework not in ALLOWED_FRAMEWORKS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Framework must be one of {ALLOWED_FRAMEWORKS}"
            )

        # Validate file extension
        if not validate_model_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File must have one of these extensions: {ALLOWED_EXTENSIONS}"
            )

        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{model_info.name}_{timestamp}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join(MODEL_STORAGE_PATH, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Get file size
        file_size = get_file_size(file_path)

        response = ModelResponse(
            id=unique_filename,
            info=model_info,
            status="uploaded",
            created_at=datetime.now().isoformat(),
            size=file_size
        )

        logger.info(f"Model {unique_filename} uploaded successfully")
        return response

    except Exception as e:
        logger.error(f"Error uploading model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/list", response_model=List[ModelResponse])
async def list_models(
    framework: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all available models with optional framework filter
    """
    try:
        models = []
        for filename in os.listdir(MODEL_STORAGE_PATH):
            if not validate_model_file(filename):
                continue

            file_path = os.path.join(MODEL_STORAGE_PATH, filename)
            file_stats = os.stat(file_path)

            # Extract model info from filename
            name_parts = os.path.splitext(filename)[0].split('_')
            model_name = name_parts[0]
            
            model = ModelResponse(
                id=filename,
                info=ModelInfo(
                    name=model_name,
                    framework="auto-detected",
                    version="1.0"
                ),
                status="available",
                created_at=datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                last_modified=datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                size=file_stats.st_size
            )

            if framework is None or model.info.framework == framework:
                models.append(model)

        return models

    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get details of a specific model
    """
    try:
        file_path = os.path.join(MODEL_STORAGE_PATH, model_id)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {model_id} not found"
            )

        file_stats = os.stat(file_path)
        name_parts = os.path.splitext(model_id)[0].split('_')
        model_name = name_parts[0]

        return ModelResponse(
            id=model_id,
            info=ModelInfo(
                name=model_name,
                framework="auto-detected",
                version="1.0"
            ),
            status="available",
            created_at=datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            last_modified=datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            size=file_stats.st_size
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{model_id}")
async def delete_model(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a model file
    """
    try:
        file_path = os.path.join(MODEL_STORAGE_PATH, model_id)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {model_id} not found"
            )

        os.remove(file_path)
        logger.info(f"Model {model_id} deleted successfully")
        
        return {"message": f"Model {model_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.patch("/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: str,
    update_data: ModelUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update model metadata
    """
    try:
        file_path = os.path.join(MODEL_STORAGE_PATH, model_id)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {model_id} not found"
            )

        file_stats = os.stat(file_path)
        name_parts = os.path.splitext(model_id)[0].split('_')
        model_name = name_parts[0]

        current_info = ModelInfo(
            name=model_name,
            framework="auto-detected",
            version="1.0"
        )

        updated_info = current_info.copy(update=update_data.info.dict(exclude_unset=True)) if update_data.info else current_info

        return ModelResponse(
            id=model_id,
            info=updated_info,
            status=update_data.status or "available",
            created_at=datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            last_modified=datetime.now().isoformat(),
            size=file_stats.st_size
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )