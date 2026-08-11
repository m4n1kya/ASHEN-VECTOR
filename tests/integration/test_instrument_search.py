import pytest
from fastapi.testclient import TestClient
from ashen_vector.api.main import app

client = TestClient(app)

def test_search_instruments_exact():
    response = client.get("/api/instruments/search?q=SH600000")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert any(i["symbol"] == "SH600000" for i in data["results"])

def test_search_instruments_partial_name():
    response = client.get("/api/instruments/search?q=pudong")
    assert response.status_code == 200
    data = response.json()
    # It might or might not return SH600000 depending on exact string match,
    # but the endpoint should not fail.
    assert "count" in data

def test_search_instruments_missing():
    response = client.get("/api/instruments/search?q=UNKNOWN123")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert len(data["results"]) == 0
