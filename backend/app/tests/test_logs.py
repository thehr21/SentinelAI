import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_log_submission():
    response = client.post("/logs", json={
        "username": "tester",
        "ip_address": "127.0.0.1",
        "action": "login",
        "result": "success",
        "endpoint": "/login"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_invalid_log_submission():
    response = client.post("/logs", json={
        "username": "missing_fields"
        # missing ip_address, action, result, endpoint
    })
    assert response.status_code == 422

def test_get_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
