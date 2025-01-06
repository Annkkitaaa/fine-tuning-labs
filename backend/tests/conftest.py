import pytest
import numpy as np
import torch
from pathlib import Path

@pytest.fixture
def sample_data():
    return np.random.randn(100, 10)

@pytest.fixture
def sample_model():
    return torch.nn.Sequential(
        torch.nn.Linear(10, 5),
        torch.nn.ReLU(),
        torch.nn.Linear(5, 2)
    )
