import pytest
from fastapi.testclient import TestClient

from ashen_vector.api.main import app

client = TestClient(app)

def test_get_features_success():
    """Verify the /api/stocks/{symbol}/features endpoint."""
    response = client.get("/api/stocks/SH600000/features?start_date=2020-03-01&end_date=2020-03-31")
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["symbol"] == "SH600000"
    assert "features" in data
    assert data["feature_count"] > 0
    
    # Check that we have a decent number of days returned (should be ~22 trading days in a month)
    features = data["features"]
    assert len(features) > 15
    
    # Check some specific features exist
    first_row = features[0]
    assert "date" in first_row
    assert "return_1d" in first_row
    assert "macd" in first_row
    assert "rsi_14" in first_row
    
def test_get_analytics_success():
    """Verify the /api/stocks/{symbol}/analytics endpoint."""
    response = client.get("/api/stocks/SH600000/analytics?start_date=2020-03-01&end_date=2020-03-31")
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["symbol"] == "SH600000"
    assert data["total_return"] is not None
    assert data["sharpe_ratio"] is not None
    assert data["volatility"] is not None
