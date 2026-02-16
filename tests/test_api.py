import pytest
import json
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/api/v1/health')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_classification_train_endpoint(client):
    response = client.post('/api/v1/classification/train', 
                           json={"n_samples": 100, "n_features": 5})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert 'metrics' in data

def test_regression_train_endpoint(client):
    response = client.post('/api/v1/regression/train', 
                           json={"n_samples": 100, "n_features": 5})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'success'

def test_classification_predict_endpoint(client):
    # Primeiro treinar
    client.post('/api/v1/classification/train', json={"n_samples": 50})
    # Depois predizer
    response = client.post('/api/v1/classification/predict', 
                           json={"data": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "predictions" in data

def test_regression_predict_endpoint(client):
    client.post('/api/v1/regression/train', json={"n_samples": 50})
    response = client.post('/api/v1/regression/predict', 
                           json={"data": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "predictions" in data

def test_classification_explain_endpoint(client):
    client.post('/api/v1/classification/train', json={"n_samples": 50})
    response = client.post('/api/v1/classification/explain', 
                           json={"data": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]], "sample_idx": 0})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "explanation" in data

