import pytest
from fastapi.testclient import TestClient
from ashen_vector.api.main import app

client = TestClient(app)

def test_models_metadata_endpoint():
    response = client.get("/api/stocks/SH600000/models")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "SH600000"
    assert "models" in data
    assert isinstance(data["models"], list)

def test_models_metadata_invalid_symbol():
    response = client.get("/api/stocks/INVALID_SYM/models")
    assert response.status_code == 404
