from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    roc_auc_score, confusion_matrix, mean_squared_error,
    r2_score, f1_score
)
import tensorflow as tf
import torch

class ModelEvaluator:
    def __init__(self):
        self.metrics_history: List[Dict[str, float]] = []
        self.supported_tasks = ['classification', 'regression']
        
    def evaluate(
        self,
        y_true: Union[np.ndarray, torch.Tensor, tf.Tensor],
        y_pred: Union[np.ndarray, torch.Tensor, tf.Tensor],
        task_type: str = 'classification',
        threshold: float = 0.5
    ) -> Dict[str, float]:
        # Convert inputs to numpy arrays
        y_true = self._to_numpy(y_true)
        y_pred = self._to_numpy(y_pred)
        
        if task_type == 'classification':
            if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
                y_pred_classes = np.argmax(y_pred, axis=1)
            else:
                y_pred_classes = (y_pred > threshold).astype(int)
            
            metrics = self._compute_classification_metrics(y_true, y_pred_classes, y_pred)
        elif task_type == 'regression':
            metrics = self._compute_regression_metrics(y_true, y_pred)
        else:
            raise ValueError(f"Task type must be one of {self.supported_tasks}")
        
        self.metrics_history.append(metrics)
        return metrics
    
    def _compute_classification_metrics(
        self,
        y_true: np.ndarray,
        y_pred_classes: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict[str, float]:
        metrics = {}
        
        # Basic classification metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred_classes)
        
        # Precision, recall, F1
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred_classes, average='weighted'
        )
        metrics.update({
            'precision': precision,
            'recall': recall,
            'f1': f1
        })
        
        # ROC AUC (for binary classification)
        if len(np.unique(y_true)) == 2:
            try:
                metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
            except ValueError:
                pass
        
        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred_classes)
        metrics['confusion_matrix'] = cm.tolist()
        
        return metrics
    
    def _compute_regression_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, float]:
        return {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mae': np.mean(np.abs(y_true - y_pred))
        }
    
    def _to_numpy(
        self,
        tensor: Union[np.ndarray, torch.Tensor, tf.Tensor]
    ) -> np.ndarray:
        if isinstance(tensor, torch.Tensor):
            return tensor.detach().cpu().numpy()
        elif isinstance(tensor, tf.Tensor):
            return tensor.numpy()
        return tensor
    
    def get_metrics_summary(self) -> Dict[str, Dict[str, float]]:
        if not self.metrics_history:
            return {}
            
        metrics = {}
        for key in self.metrics_history[0].keys():
            if key != 'confusion_matrix':
                values = [m[key] for m in self.metrics_history]
                metrics[key] = {
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values))
                }
        return metrics
    
    def reset_history(self) -> None:
        self.metrics_history = []