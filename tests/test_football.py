import pytest
import football

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test homepage route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data  # Check homepage is working correctlys

def test_top_scorers(client):
    """Test top scorers route."""
    response = client.get('/top_scorers')
    assert response.status_code == 200
    assert len(response.get_json()) == 5  # Check the response contains data for the top 5 scorers

def test_top_assists(client):
    """Test top assists route."""
    response = client.get('/top_assists')
    assert response.status_code == 200
    assert len(response.get_json()) == 5  # Check the response contains data for the top 5 assists

def test_average_passes(client):
    """Test average passes route."""
    response = client.get('/average_passes')
    assert response.status_code == 200
    assert 'average_passes' in response.get_json()  # Ensure 'average_passes' key exists

def test_defensive_contributions(client):
    """Test defensive contributions route."""
    response = client.get('/defensive_contributions')
    assert response.status_code == 200
    assert len(response.get_json()) == 5  # Check the response contains data for the top 5 defensive contributions

