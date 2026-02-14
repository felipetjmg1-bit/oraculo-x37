import pytest
import numpy as np
import os
from oracle_model import OracleX37, generate_sample_data

def test_generate_data():
    X, y = generate_sample_data(n_samples=100, n_features=5, task="classification")
    assert X.shape == (100, 5)
    assert y.shape == (100,)
    assert len(np.unique(y)) <= 2

def test_classification_flow():
    oracle = OracleX37(model_type="classification")
    X, y = generate_sample_data(n_samples=200, n_features=10, task="classification")
    
    # Test training
    metrics = oracle.train(X, y)
    assert "accuracy" in metrics
    assert oracle.is_trained is True
    
    # Test prediction
    preds = oracle.predict(X[:5])
    assert len(preds) == 5
    
    # Test explainability
    explanation = oracle.explain_prediction(X, sample_idx=0)
    assert "prediction" in explanation
    assert "top_features" in explanation
    assert len(explanation["top_features"]) <= 5

def test_regression_flow():
    oracle = OracleX37(model_type="regression")
    X, y = generate_sample_data(n_samples=200, n_features=10, task="regression")
    
    # Test training
    metrics = oracle.train(X, y)
    assert "r2_score" in metrics
    assert oracle.is_trained is True
    
    # Test prediction
    preds = oracle.predict(X[:5])
    assert len(preds) == 5

def test_save_load():
    oracle = OracleX37(model_type="classification")
    X, y = generate_sample_data(n_samples=100, n_features=5, task="classification")
    oracle.train(X, y)
    
    model_path = "test_model.pkl"
    oracle.save_model(model_path)
    assert os.path.exists(model_path)
    
    new_oracle = OracleX37(model_type="classification")
    new_oracle.load_model(model_path)
    assert new_oracle.is_trained is True
    
    # Cleanup
    if os.path.exists(model_path):
        os.remove(model_path)
