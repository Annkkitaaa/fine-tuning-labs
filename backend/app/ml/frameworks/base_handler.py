from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModelHandler(ABC):
    @abstractmethod
    def load_model(self, path: str) -> Any:
        pass
    
    @abstractmethod
    def save_model(self, model: Any, path: str) -> str:
        pass
    
    @abstractmethod
    def predict(self, model: Any, data: Any) -> Any:
        pass