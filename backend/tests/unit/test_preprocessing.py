import pytest
import numpy as np
from app.api.utils.preprocessing import DataPreprocessor

def test_numerical_preprocessing():
    preprocessor = DataPreprocessor()
    data = np.array([[1.0, 2.0], [3.0, 4.0]])
    columns = ['col1', 'col2']
    processed_data = preprocessor.preprocess_numerical(data, columns)
    assert processed_data.shape == data.shape
    assert np.allclose(processed_data.mean(axis=0), [0, 0], atol=1e-10)

def test_categorical_preprocessing():
    preprocessor = DataPreprocessor()
    data = np.array([['a', 'b'], ['b', 'c']])
    columns = ['col1', 'col2']
    processed_data = preprocessor.preprocess_categorical(data, columns)
    assert processed_data.shape == data.shape
    assert processed_data.dtype == np.int64