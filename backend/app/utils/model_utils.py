import os
import json
from typing import Dict, Any

def save_model_config(model_id: str, config: Dict[str, Any]) -> str:
    config_path = f"models/{model_id}/config.json"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f)
    return config_path

def load_model_config(model_id: str) -> Dict[str, Any]:
    config_path = f"models/{model_id}/config.json"
    with open(config_path, "r") as f:
        return json.load(f)