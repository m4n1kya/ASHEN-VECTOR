import pytest
from fastapi.testclient import TestClient
from ashen_vector.api.main import app

client = TestClient(app)

def test_backtest_endpoint():
    response = client.get("/api/stocks/SH600000/backtest")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "NOT_AVAILABLE"
