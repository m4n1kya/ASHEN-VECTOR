import pytest
from fastapi.testclient import TestClient
from ashen_vector.api.main import app

client = TestClient(app)

def test_prediction_endpoint_unavailable():
    """Test prediction for an instrument/model that doesn't exist."""
    payload = {
        "symbol": "SH600000",
        "horizon": 5,
        "classifier_id": "nonexistent_model_id"
    }
    response = client.post("/api/predictions/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"]["status"] == "MODEL_UNAVAILABLE"
    assert data["prediction"]["direction"] is None
