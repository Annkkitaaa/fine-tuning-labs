import numpy as np
from typing import Tuple, Any
import torch
import tensorflow as tf

def prepare_data(data: Any, framework: str) -> Tuple[Any, Any]:
    if framework == "pytorch":
        return prepare_pytorch_data(data)
    elif framework == "tensorflow":
        return prepare_tensorflow_data(data)
    return prepare_sklearn_data(data)