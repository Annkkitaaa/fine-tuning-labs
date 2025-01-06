import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_model_upload():
    response = client.post(
        "/api/v1/models/upload",
        files={"file": ("model.pt", b"test content", "application/octet-stream")}
    )
    assert response.status_code == 200
    assert "filename" in response.json()

def test_training_workflow():
    # Start training
    training_config = {
        "model_id": "test_model",
        "dataset_path": "test_data.csv",
        "hyperparameters": {"epochs": 1}
    }
    response = client.post("/api/v1/training/start", json=training_config)
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    
    # Check status
    response = client.get(f"/api/v1/training/status/{job_id}")
    assert response.status_code == 200
    assert "status" in response.json()
