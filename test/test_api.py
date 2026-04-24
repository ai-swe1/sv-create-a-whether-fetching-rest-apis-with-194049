import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_weather_valid_city():
    response = client.get('/weather?q=London')
    assert response.status_code == 200
    assert 'weather' in response.json()

def test_get_weather_invalid_city():
    response = client.get('/weather?q=InvalidCity')
    assert response.status_code == 400

def test_get_root Returns_200_and_html():
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['Content-Type']