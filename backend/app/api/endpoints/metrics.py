from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from pydantic import BaseModel
from ..core.security import get_current_user
from ..ml.evaluation.metrics import ModelEvaluator

router = APIRouter()

class MetricsRequest(BaseModel):
    model_id: str
    dataset_path: str

class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float

@router.post("/evaluate", response_model=MetricsResponse)
async def evaluate_model(
    request: MetricsRequest,
    current_user = Depends(get_current_user)
):
    try:
        evaluator = ModelEvaluator()
        # In practice, load model and dataset here
        metrics = evaluator.compute_metrics(
            y_true=[1, 0, 1, 1, 0],
            y_pred=[1, 0, 1, 0, 0]
        )
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{model_id}", response_model=List[MetricsResponse])
async def get_metrics_history(
    model_id: str,
    current_user = Depends(get_current_user)
):
    try:
        evaluator = ModelEvaluator()
        return evaluator.get_metric_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))