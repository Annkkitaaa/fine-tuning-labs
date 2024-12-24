import torch
import tensorflow as tf
from typing import Dict, Any, Optional
import mlflow
import numpy as np

class FineTuningManager:
    def __init__(self, framework: str = "pytorch"):
        self.framework = framework
        self.model = None
        self.optimizer = None
        
    def load_model(self, model_path: str) -> Any:
        if self.framework == "pytorch":
            self.model = torch.load(model_path)
        elif self.framework == "tensorflow":
            self.model = tf.keras.models.load_model(model_path)
        return self.model
        
    def fine_tune(self, 
                 train_data: Any, 
                 val_data: Optional[Any] = None,
                 epochs: int = 10,
                 batch_size: int = 32) -> Dict[str, Any]:
        
        if self.framework == "pytorch":
            return self._fine_tune_pytorch(train_data, val_data, epochs, batch_size)
        elif self.framework == "tensorflow":
            return self._fine_tune_tensorflow(train_data, val_data, epochs, batch_size)
    
    def evaluate_model(self):
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(self.y_test, self.model.predict(self.X_test))
        mlflow.log_metrics(metrics)
        return metrics