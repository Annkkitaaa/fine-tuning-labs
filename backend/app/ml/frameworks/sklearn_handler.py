from sklearn.base import BaseEstimator
import joblib
from typing import Any, Dict
import numpy as np
from .base_handler import BaseModelHandler

class SklearnHandler(BaseModelHandler):
    def load_model(self, path: str) -> BaseEstimator:
        return joblib.load(path)
    
    def save_model(self, model: BaseEstimator, path: str) -> str:
        joblib.dump(model, path)
        return path
    
    def predict(self, model: BaseEstimator, data: np.ndarray) -> np.ndarray:
        return model.predict(data)
    
    def train(
        self,
        model: BaseEstimator,
        X_train: np.ndarray,
        y_train: np.ndarray,
        **kwargs
    ) -> Dict:
        model.fit(X_train, y_train, **kwargs)
        train_score = model.score(X_train, y_train)
        return {'train_score': train_score}
    
    def get_params(self, model: BaseEstimator) -> Dict:
        return model.get_params()
    
    def set_params(self, model: BaseEstimator, **params) -> BaseEstimator:
        return model.set_params(**params)