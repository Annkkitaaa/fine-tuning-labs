import pytest
import torch
from app.ml.frameworks.pytorch_handler import PyTorchHandler

def test_pytorch_handler():
    handler = PyTorchHandler()
    model = torch.nn.Linear(10, 2)
    data = torch.randn(5, 10)
    output = handler.predict(model, data)
    assert output.shape == (5, 2)
