from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
from typing import Dict, Any

class ModelEvaluator:
    def __init__(self):
        self.metrics = {}
        
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        self.metrics["accuracy"] = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        
        self.metrics.update({
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
        
        return self.metrics
        
    def get_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        from sklearn.metrics import confusion_matrix
        return confusion_matrix(y_true, y_pred)
        
    def get_classification_report(self, y_true: np.ndarray, y_pred: np.ndarray) -> str:
        from sklearn.metrics import classification_report
        return classification_report(y_true, y_pred)