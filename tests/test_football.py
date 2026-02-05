import sys
import os

# Ensure the parent directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from football import app  # Import the app variable from football.py
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test homepage route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data  # Check homepage is working correctly

def test_top_scorers(client):
    """Test top scorers route."""
    response = client.get('/top_scorers')
    assert response.status_code == 200
    assert b'Player' in response.data  # Check if the word 'Player' exists in code



