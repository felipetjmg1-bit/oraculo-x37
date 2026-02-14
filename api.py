"""
API REST para o Oráculo X-37

Fornece endpoints para treinar, fazer predições e explicar resultados do modelo.
"""

from flask import Flask, request, jsonify
from oracle_model import OracleX37, generate_sample_data
import numpy as np
import traceback

app = Flask(__name__)

# Instâncias globais dos modelos
oracle_clf = None
oracle_reg = None


@app.route('/health', methods=['GET'])
def health():
    """Verifica o status da API."""
    return jsonify({
        "status": "healthy",
        "message": "Oráculo X-37 API está operacional",
        "version": "1.0.0"
    })


@app.route('/api/v1/classification/train', methods=['POST'])
def train_classification():
    """
    Treina um modelo de classificação.
    
    Body JSON:
    {
        "n_samples": 1000,
        "n_features": 10,
        "test_size": 0.2
    }
    """
    global oracle_clf
    
    try:
        data = request.get_json()
        n_samples = data.get('n_samples', 1000)
        n_features = data.get('n_features', 10)
        test_size = data.get('test_size', 0.2)
        
        # Gerar dados
        X, y = generate_sample_data(n_samples, n_features, task="classification")
        
        # Criar e treinar modelo
        oracle_clf = OracleX37(model_type="classification")
        oracle_clf.set_feature_names([f"Feature_{i}" for i in range(n_features)])
        
        metrics = oracle_clf.train(X, y, test_size=test_size)
        
        return jsonify({
            "status": "success",
            "message": "Modelo de classificação treinado com sucesso",
            "metrics": metrics,
            "n_samples": n_samples,
            "n_features": n_features
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/regression/train', methods=['POST'])
def train_regression():
    """
    Treina um modelo de regressão.
    
    Body JSON:
    {
        "n_samples": 1000,
        "n_features": 10,
        "test_size": 0.2
    }
    """
    global oracle_reg
    
    try:
        data = request.get_json()
        n_samples = data.get('n_samples', 1000)
        n_features = data.get('n_features', 10)
        test_size = data.get('test_size', 0.2)
        
        # Gerar dados
        X, y = generate_sample_data(n_samples, n_features, task="regression")
        
        # Criar e treinar modelo
        oracle_reg = OracleX37(model_type="regression")
        oracle_reg.set_feature_names([f"Feature_{i}" for i in range(n_features)])
        
        metrics = oracle_reg.train(X, y, test_size=test_size)
        
        return jsonify({
            "status": "success",
            "message": "Modelo de regressão treinado com sucesso",
            "metrics": metrics,
            "n_samples": n_samples,
            "n_features": n_features
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/classification/predict', methods=['POST'])
def predict_classification():
    """
    Faz predições com o modelo de classificação.
    
    Body JSON:
    {
        "data": [[1.0, 2.0, 3.0, ...], ...]
    }
    """
    global oracle_clf
    
    try:
        if oracle_clf is None or not oracle_clf.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de classificação não foi treinado"
            }), 400
        
        data = request.get_json()
        X = np.array(data['data'])
        
        predictions = oracle_clf.predict(X)
        probabilities = oracle_clf.predict_proba(X)
        
        return jsonify({
            "status": "success",
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist(),
            "n_samples": len(predictions)
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/regression/predict', methods=['POST'])
def predict_regression():
    """
    Faz predições com o modelo de regressão.
    
    Body JSON:
    {
        "data": [[1.0, 2.0, 3.0, ...], ...]
    }
    """
    global oracle_reg
    
    try:
        if oracle_reg is None or not oracle_reg.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de regressão não foi treinado"
            }), 400
        
        data = request.get_json()
        X = np.array(data['data'])
        
        predictions = oracle_reg.predict(X)
        
        return jsonify({
            "status": "success",
            "predictions": predictions.tolist(),
            "n_samples": len(predictions)
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/classification/explain', methods=['POST'])
def explain_classification():
    """
    Explica uma predição do modelo de classificação.
    
    Body JSON:
    {
        "data": [[1.0, 2.0, 3.0, ...]],
        "sample_idx": 0
    }
    """
    global oracle_clf
    
    try:
        if oracle_clf is None or not oracle_clf.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de classificação não foi treinado"
            }), 400
        
        data = request.get_json()
        X = np.array(data['data'])
        sample_idx = data.get('sample_idx', 0)
        
        explanation = oracle_clf.explain_prediction(X, sample_idx=sample_idx)
        
        return jsonify({
            "status": "success",
            "explanation": explanation
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/regression/explain', methods=['POST'])
def explain_regression():
    """
    Explica uma predição do modelo de regressão.
    
    Body JSON:
    {
        "data": [[1.0, 2.0, 3.0, ...]],
        "sample_idx": 0
    }
    """
    global oracle_reg
    
    try:
        if oracle_reg is None or not oracle_reg.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de regressão não foi treinado"
            }), 400
        
        data = request.get_json()
        X = np.array(data['data'])
        sample_idx = data.get('sample_idx', 0)
        
        explanation = oracle_reg.explain_prediction(X, sample_idx=sample_idx)
        
        return jsonify({
            "status": "success",
            "explanation": explanation
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/classification/feature-importance', methods=['GET'])
def get_classification_feature_importance():
    """Retorna a importância das features do modelo de classificação."""
    global oracle_clf
    
    try:
        if oracle_clf is None or not oracle_clf.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de classificação não foi treinado"
            }), 400
        
        top_n = request.args.get('top_n', 10, type=int)
        importances = oracle_clf.get_feature_importance(top_n=top_n)
        
        return jsonify({
            "status": "success",
            "feature_importance": importances
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/regression/feature-importance', methods=['GET'])
def get_regression_feature_importance():
    """Retorna a importância das features do modelo de regressão."""
    global oracle_reg
    
    try:
        if oracle_reg is None or not oracle_reg.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de regressão não foi treinado"
            }), 400
        
        top_n = request.args.get('top_n', 10, type=int)
        importances = oracle_reg.get_feature_importance(top_n=top_n)
        
        return jsonify({
            "status": "success",
            "feature_importance": importances
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/classification/metrics', methods=['GET'])
def get_classification_metrics():
    """Retorna as métricas de treinamento do modelo de classificação."""
    global oracle_clf
    
    try:
        if oracle_clf is None or not oracle_clf.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de classificação não foi treinado"
            }), 400
        
        metrics = oracle_clf.get_metrics()
        
        return jsonify({
            "status": "success",
            "metrics": metrics
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.route('/api/v1/regression/metrics', methods=['GET'])
def get_regression_metrics():
    """Retorna as métricas de treinamento do modelo de regressão."""
    global oracle_reg
    
    try:
        if oracle_reg is None or not oracle_reg.is_trained:
            return jsonify({
                "status": "error",
                "message": "Modelo de regressão não foi treinado"
            }), 400
        
        metrics = oracle_reg.get_metrics()
        
        return jsonify({
            "status": "success",
            "metrics": metrics
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 400


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas."""
    return jsonify({
        "status": "error",
        "message": "Rota não encontrada"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos."""
    return jsonify({
        "status": "error",
        "message": "Erro interno do servidor"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🔮 Oráculo X-37 - API REST")
    print("=" * 60)
    print("\nIniciando servidor em http://localhost:5000")
    print("\nEndpoints disponíveis:")
    print("  GET  /health")
    print("  POST /api/v1/classification/train")
    print("  POST /api/v1/regression/train")
    print("  POST /api/v1/classification/predict")
    print("  POST /api/v1/regression/predict")
    print("  POST /api/v1/classification/explain")
    print("  POST /api/v1/regression/explain")
    print("  GET  /api/v1/classification/feature-importance")
    print("  GET  /api/v1/regression/feature-importance")
    print("  GET  /api/v1/classification/metrics")
    print("  GET  /api/v1/regression/metrics")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
