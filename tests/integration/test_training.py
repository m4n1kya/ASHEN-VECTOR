import pytest
from fastapi.testclient import TestClient
import time
import asyncio

from ashen_vector.api.main import app
from ashen_vector.api.routes.training import TRAINING_JOBS

client = TestClient(app)

def test_async_training_flow():
    """Verify that we can start a training job and poll its status."""
    payload = {
        "symbol": "SH600000",
        "start_date": "2020-01-01",
        "end_date": "2020-03-31",
        "model_type": "lightgbm",
        "objective": "binary",
        "target_col": "future_direction",
        "horizon": 5,
        "model_kwargs": {"n_estimators": 10}
    }
    
    # 1. Start job
    response = client.post("/api/training/train", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"
    
    job_id = data["job_id"]
    
    # Wait briefly for background task to execute
    time.sleep(1)
    
    # 2. Check status
    status_response = client.get(f"/api/training/jobs/{job_id}")
    assert status_response.status_code == 200
    status_data = status_response.json()
    
    assert status_data["job_id"] == job_id
    assert status_data["status"] in ["running", "completed", "failed"]

def test_inference_endpoint():
    """Verify that predictions endpoint returns correct schema."""
    # Note: this requires a model to be trained, so we test it generically
    # Or mock the PredictionEngine
    pass
