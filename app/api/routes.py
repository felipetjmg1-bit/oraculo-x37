from flask import Blueprint, request, jsonify
import numpy as np
import traceback
from app.services.oracle_service import OracleService, generate_sample_data
from app.core.config import settings

api_bp = Blueprint('api', __name__)

# Instâncias globais (Lazy loading ou inicialização via config)
oracle_clf = OracleService(model_type="classification")
oracle_reg = OracleService(model_type="regression")

# Tentar carregar modelos existentes
oracle_clf.load(settings.DEFAULT_CLF_MODEL_PATH)
oracle_reg.load(settings.DEFAULT_REG_MODEL_PATH)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": f"{settings.PROJECT_NAME} API operacional",
        "version": settings.VERSION
    })

@api_bp.route('/classification/train', methods=['POST'])
def train_classification():
    try:
        data = request.get_json() or {}
        n_samples = data.get('n_samples', 1000)
        n_features = data.get('n_features', 10)
        test_size = data.get('test_size', 0.2)
        
        X, y = generate_sample_data(n_samples, n_features, task="classification")
        oracle_clf.feature_names = [f"Feature_{i}" for i in range(n_features)]
        metrics = oracle_clf.train(X, y, test_size=test_size)
        
        # Opcional: Salvar após treinar
        oracle_clf.save(settings.DEFAULT_CLF_MODEL_PATH)
        
        return jsonify({"status": "success", "metrics": metrics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@api_bp.route('/regression/train', methods=['POST'])
def train_regression():
    try:
        data = request.get_json() or {}
        n_samples = data.get('n_samples', 1000)
        n_features = data.get('n_features', 10)
        test_size = data.get('test_size', 0.2)
        
        X, y = generate_sample_data(n_samples, n_features, task="regression")
        oracle_reg.feature_names = [f"Feature_{i}" for i in range(n_features)]
        metrics = oracle_reg.train(X, y, test_size=test_size)
        
        oracle_reg.save(settings.DEFAULT_REG_MODEL_PATH)
        
        return jsonify({"status": "success", "metrics": metrics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@api_bp.route('/classification/predict', methods=['POST'])
def predict_classification():
    try:
        if not oracle_clf.is_trained:
            return jsonify({"status": "error", "message": "Modelo não treinado"}), 400
        data = request.get_json()
        X = np.array(data['data'])
        predictions = oracle_clf.predict(X)
        probabilities = oracle_clf.predict_proba(X)
        return jsonify({
            "status": "success",
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist()
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@api_bp.route('/regression/predict', methods=['POST'])
def predict_regression():
    try:
        if not oracle_reg.is_trained:
            return jsonify({"status": "error", "message": "Modelo não treinado"}), 400
        data = request.get_json()
        X = np.array(data['data'])
        predictions = oracle_reg.predict(X)
        return jsonify({"status": "success", "predictions": predictions.tolist()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@api_bp.route('/classification/explain', methods=['POST'])
def explain_classification():
    try:
        if not oracle_clf.is_trained:
            return jsonify({"status": "error", "message": "Modelo não treinado"}), 400
        data = request.get_json()
        X = np.array(data['data'])
        sample_idx = data.get('sample_idx', 0)
        explanation = oracle_clf.explain_prediction(X, sample_idx=sample_idx)
        return jsonify({"status": "success", "explanation": explanation}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
