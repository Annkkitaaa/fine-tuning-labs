import pytest
from app.ml.training.hyperparameter import HyperparameterTuner
from app.ml.evaluation.metrics import ModelEvaluator

def test_training_pipeline():
    # Setup test data and model
    X_train = np.random.randn(100, 10)
    y_train = np.random.randint(0, 2, 100)
    
    # Test hyperparameter tuning
    param_space = {
        'n_estimators': {'type': 'int', 'low': 10, 'high': 100},
        'max_depth': {'type': 'int', 'low': 3, 'high': 10}
    }
    
    tuner = HyperparameterTuner(RandomForestClassifier, X_train, y_train)
    results = tuner.optimize(param_space, n_trials=5)
    assert 'best_params' in results
    
    # Test model evaluation
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate(y_train[:10], y_train[:10])
    assert metrics['accuracy'] == 1.0