# backend/app/core/hyperparameter_tuning.py

from optuna import create_study, Trial
import mlflow
from typing import Dict, Any, Callable
import torch
import tensorflow as tf
from sklearn.model_selection import GridSearchCV

class HyperparameterTuner:
   def __init__(self, framework: str):
       self.framework = framework
       
   def optimize(self, 
               objective_fn: Callable,
               n_trials: int = 20,
               param_space: Dict[str, Any] = None) -> Dict[str, Any]:
       study = create_study(direction="minimize")
       param_space = param_space or self._default_param_space()
       
       def objective(trial: Trial):
           params = {}
           for name, space in param_space.items():
               if space["type"] == "float":
                   params[name] = trial.suggest_float(
                       name, space["low"], space["high"], log=space.get("log", True)
                   )
               elif space["type"] == "categorical":
                   params[name] = trial.suggest_categorical(name, space["choices"])
               elif space["type"] == "int":
                   params[name] = trial.suggest_int(
                       name, space["low"], space["high"], step=space.get("step", 1)
                   )
           
           with mlflow.start_run(nested=True):
               mlflow.log_params(params)
               return objective_fn(params)
               
       study.optimize(objective, n_trials=n_trials)
       return study.best_params

   def _default_param_space(self) -> Dict[str, Any]:
       if self.framework == "pytorch":
           return {
               "learning_rate": {"type": "float", "low": 1e-5, "high": 1e-1, "log": True},
               "batch_size": {"type": "categorical", "choices": [16, 32, 64, 128]},
               "optimizer": {"type": "categorical", "choices": ["adam", "sgd", "adamw"]},
               "weight_decay": {"type": "float", "low": 1e-6, "high": 1e-2, "log": True},
               "dropout_rate": {"type": "float", "low": 0.1, "high": 0.5},
               "num_layers": {"type": "int", "low": 1, "high": 5}
           }
       elif self.framework == "tensorflow":
           return {
               "learning_rate": {"type": "float", "low": 1e-5, "high": 1e-1, "log": True},
               "batch_size": {"type": "categorical", "choices": [16, 32, 64, 128]},
               "optimizer": {"type": "categorical", "choices": ["adam", "rmsprop", "sgd"]},
               "activation": {"type": "categorical", "choices": ["relu", "elu", "tanh"]},
               "num_units": {"type": "int", "low": 32, "high": 512, "step": 32}
           }
       elif self.framework == "sklearn":
           return {
               "max_depth": {"type": "int", "low": 3, "high": 10},
               "min_samples_split": {"type": "int", "low": 2, "high": 10},
               "min_samples_leaf": {"type": "int", "low": 1, "high": 4},
               "n_estimators": {"type": "int", "low": 100, "high": 1000, "step": 100}
           }

   def get_optimizer(self, params: Dict[str, Any], model: Any) -> Any:
       if self.framework == "pytorch":
           optimizer_name = params.get("optimizer", "adam").lower()
           lr = params.get("learning_rate", 0.001)
           
           if optimizer_name == "adam":
               return torch.optim.Adam(model.parameters(), lr=lr)
           elif optimizer_name == "sgd":
               return torch.optim.SGD(model.parameters(), lr=lr)
           elif optimizer_name == "adamw":
               return torch.optim.AdamW(model.parameters(), lr=lr)
               
       elif self.framework == "tensorflow":
           optimizer_name = params.get("optimizer", "adam").lower()
           lr = params.get("learning_rate", 0.001)
           
           if optimizer_name == "adam":
               return tf.keras.optimizers.Adam(learning_rate=lr)
           elif optimizer_name == "rmsprop":
               return tf.keras.optimizers.RMSprop(learning_rate=lr)
           elif optimizer_name == "sgd":
               return tf.keras.optimizers.SGD(learning_rate=lr)

   def grid_search(self, model, param_grid: Dict[str, Any], X, y):
       if self.framework == "sklearn":
           search = GridSearchCV(
               model, 
               param_grid,
               cv=5,
               n_jobs=-1,
               verbose=1
           )
           search.fit(X, y)
           return search.best_params_