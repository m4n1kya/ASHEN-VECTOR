import pytest
from fastapi.testclient import TestClient
from ashen_vector.api.main import app
import math

client = TestClient(app)

def test_overview_endpoint_success():
    """Test overview endpoint with a known valid symbol."""
    response = client.get("/api/stocks/SH600000/overview")
    assert response.status_code == 200, response.text
    data = response.json()
    
    assert "instrument" in data
    assert data["instrument"]["symbol"] == "SH600000"
    
    assert "market" in data
    assert "latest_date" in data["market"]
    
    assert "performance" in data
    assert "risk" in data
    assert "technical" in data
    
    assert "data_quality" in data
    assert "trading_days_stale" in data["data_quality"]
    
    assert "prediction" in data
    assert data["prediction"]["status"] in ["ACTIVE", "MODEL_UNAVAILABLE", "MODEL_UNAVAILABLE_STALE_DATA"]
    
    # Check for NaNs
    text_data = response.text
    assert "NaN" not in text_data, "NaN found in response"
    assert "Infinity" not in text_data, "Infinity found in response"

def test_overview_endpoint_invalid_symbol():
    """Test overview endpoint with an invalid symbol."""
    response = client.get("/api/stocks/INVALID_SYM/overview")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_latest_features_endpoint():
    """Test /features/latest endpoint."""
    response = client.get("/api/stocks/SH600000/features/latest")
    assert response.status_code == 200, response.text
    data = response.json()
    
    assert "symbol" in data
    assert "date" in data
    assert "features" in data
    assert len(data["features"]) > 0
    
    # Test for forbidden columns
    forbidden = {"future_direction", "future_return", "label", "target"}
    keys = set(data["features"].keys())
    assert not forbidden.intersection(keys), "Forbidden feature found!"
