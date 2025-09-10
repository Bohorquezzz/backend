"""
Basic tests for the UpDaily API
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_docs():
    """Test that docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
