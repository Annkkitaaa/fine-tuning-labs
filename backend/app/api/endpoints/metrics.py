from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ValidationError
from app.core.security import get_current_user
import logging
from datetime import datetime
import csv
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models
class MetricsRequest(BaseModel):
    model_id: str = Field(..., description="Unique identifier for the model")
    dataset_path: str = Field(..., description="Path to the dataset")

class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion_matrix: Optional[List[List[int]]] = None

class EvaluationMetrics(BaseModel):
    model_id: str
    metrics: Dict[str, float]
    timestamp: str
    dataset_name: Optional[str] = None

class MetricsSummary(BaseModel):
    overall: Dict[str, float]
    by_framework: Dict[str, float]

class CustomMetricResponse(BaseModel):
    model_id: str
    metric_name: str
    value: float
    parameters: Dict[str, Any]

# Store metrics history
metrics_history: Dict[str, List[EvaluationMetrics]] = {}

@router.post("/evaluate", response_model=MetricsResponse)
async def evaluate_model(
    request: MetricsRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Evaluate a model on a given dataset
    """
    try:
        # Validate dataset path (example: add actual validation in production)
        if not request.dataset_path:
            raise HTTPException(
                status_code=400,
                detail="Dataset path is required"
            )
        
        # Simulate model evaluation
        metrics = {
            "accuracy": 0.95,
            "precision": 0.94,
            "recall": 0.93,
            "f1": 0.935,
            "confusion_matrix": [
                [100, 5],
                [7, 88]
            ]
        }

        logger.info(f"Model {request.model_id} evaluated successfully on {request.dataset_path}")
        return MetricsResponse(**metrics)

    except ValidationError as e:
        logger.error(f"Validation error during evaluation: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error evaluating model: {str(e)}"
        )

@router.get("/history/{model_id}", response_model=List[EvaluationMetrics])
async def get_metrics_history(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get historical metrics for a specific model
    """
    if model_id not in metrics_history:
        logger.warning(f"No history found for model {model_id}")
    return metrics_history.get(model_id, [])

@router.get("/compare", response_model=Dict[str, MetricsResponse])
async def compare_models(
    model_ids: List[str] = Query(..., description="List of model IDs to compare"),
    current_user: dict = Depends(get_current_user)
):
    """
    Compare metrics between multiple models
    """
    try:
        comparison = {}
        for model_id in model_ids:
            # Simulate getting metrics for each model
            metrics = MetricsResponse(
                accuracy=0.95,
                precision=0.94,
                recall=0.93,
                f1=0.935,
                confusion_matrix=[[100, 5], [7, 88]]
            )
            comparison[model_id] = metrics
        logger.info(f"Comparison performed for models: {', '.join(model_ids)}")
        return comparison

    except Exception as e:
        logger.error(f"Error comparing models: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing models: {str(e)}"
        )

@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary(current_user: dict = Depends(get_current_user)):
    """
    Get summary statistics of model performances
    """
    try:
        summary = MetricsSummary(
            overall={
                "average_accuracy": 0.92,
                "average_f1": 0.91,
                "best_accuracy": 0.95,
                "worst_accuracy": 0.88
            },
            by_framework={
                "pytorch": 0.93,
                "tensorflow": 0.92,
                "scikit-learn": 0.90
            }
        )
        logger.info("Metrics summary retrieved successfully")
        return summary

    except Exception as e:
        logger.error(f"Error getting metrics summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics summary: {str(e)}"
        )

@router.post("/custom-metric", response_model=CustomMetricResponse)
async def compute_custom_metric(
    model_id: str,
    metric_name: str,
    metric_params: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Compute a custom metric for a model
    """
    try:
        # Validate metric parameters
        if not metric_params:
            raise HTTPException(
                status_code=400,
                detail="Metric parameters are required"
            )

        # Simulate computing custom metric
        custom_metric_value = 0.88  # Example value

        logger.info(f"Custom metric '{metric_name}' computed for model {model_id}")
        return CustomMetricResponse(
            model_id=model_id,
            metric_name=metric_name,
            value=custom_metric_value,
            parameters=metric_params
        )

    except Exception as e:
        logger.error(f"Error computing custom metric: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error computing custom metric: {str(e)}"
        )

@router.get("/export")
async def export_metrics(
    model_id: str,
    format: str = Query("json", description="Format to export metrics ('json' or 'csv')"),
    current_user: dict = Depends(get_current_user)
):
    """
    Export metrics in specified format
    """
    try:
        metrics = {
            "model_id": model_id,
            "metrics": {
                "accuracy": 0.95,
                "precision": 0.94,
                "recall": 0.93,
                "f1": 0.935
            },
            "timestamp": datetime.now().isoformat()
        }

        if format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Metric", "Value"])
            for key, value in metrics["metrics"].items():
                writer.writerow([key, value])
            logger.info(f"Metrics for model {model_id} exported in CSV format")
            return {"data": output.getvalue()}

        elif format == "json":
            logger.info(f"Metrics for model {model_id} exported in JSON format")
            return metrics

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported format. Use 'json' or 'csv'"
            )

    except Exception as e:
        logger.error(f"Error exporting metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting metrics: {str(e)}"
        )
