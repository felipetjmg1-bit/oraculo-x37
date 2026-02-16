import pytest
import numpy as np
from app.services.oracle_service import OracleService, generate_sample_data

def test_oracle_service_classification_train():
    service = OracleService(model_type="classification")
    X, y = generate_sample_data(n_samples=100, n_features=5, task="classification")
    metrics = service.train(X, y)
    
    assert service.is_trained is True
    assert "accuracy" in metrics
    assert 0 <= metrics["accuracy"] <= 1

def test_oracle_service_regression_train():
    service = OracleService(model_type="regression")
    X, y = generate_sample_data(n_samples=100, n_features=5, task="regression")
    metrics = service.train(X, y)
    
    assert service.is_trained is True
    assert "r2_score" in metrics

def test_oracle_service_predict():
    service = OracleService(model_type="classification")
    X, y = generate_sample_data(n_samples=100, n_features=5, task="classification")
    service.train(X, y)
    
    X_new = np.random.randn(5, 5)
    preds = service.predict(X_new)
    
    assert len(preds) == 5
    assert all(p in [0, 1] for p in preds)

def test_oracle_service_explain():
    service = OracleService(model_type="classification")
    X, y = generate_sample_data(n_samples=100, n_features=5, task="classification")
    service.train(X, y)
    
    explanation = service.explain_prediction(X, sample_idx=0)
    assert "top_impact_features" in explanation
    assert "prediction" in explanation
