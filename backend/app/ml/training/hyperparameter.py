from typing import Dict, Any, Callable, List, Optional
import optuna
from dataclasses import dataclass
import numpy as np
from sklearn.model_selection import cross_val_score

@dataclass
class HyperparameterSpace:
    parameters: Dict[str, Dict[str, Any]]
    constraints: Optional[List[Callable]] = None

class HyperparameterTuner:
    def __init__(self, model_creator: Callable, X: np.ndarray, y: np.ndarray):
        self.model_creator = model_creator
        self.X = X
        self.y = y
        self.study = None
        
    def objective(self, trial: optuna.Trial) -> float:
        params = {}
        for name, config in self.param_space.parameters.items():
            if config['type'] == 'categorical':
                params[name] = trial.suggest_categorical(name, config['choices'])
            elif config['type'] == 'int':
                params[name] = trial.suggest_int(name, config['low'], config['high'])
            elif config['type'] == 'float':
                params[name] = trial.suggest_float(
                    name, config['low'], config['high'], log=config.get('log', False)
                )
        
        model = self.model_creator(**params)
        scores = cross_val_score(model, self.X, self.y, cv=5)
        return scores.mean()
    
    def optimize(
        self,
        param_space: HyperparameterSpace,
        n_trials: int = 100,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        self.param_space = param_space
        self.study = optuna.create_study(direction="maximize")
        
        try:
            self.study.optimize(
                self.objective,
                n_trials=n_trials,
                timeout=timeout,
                callbacks=[self._check_constraints]
            )
        except optuna.exceptions.TrialPruned:
            pass
        
        return {
            'best_params': self.study.best_params,
            'best_value': self.study.best_value,
            'optimization_history': self.get_optimization_history()
        }
    
    def _check_constraints(self, study: optuna.Study, trial: optuna.Trial) -> None:
        if self.param_space.constraints:
            for constraint in self.param_space.constraints:
                if not constraint(trial.params):
                    raise optuna.exceptions.TrialPruned()
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        if not self.study:
            return []
        
        return [
            {
                'trial_number': t.number,
                'params': t.params,
                'value': t.value
            }
            for t in self.study.trials
        ]