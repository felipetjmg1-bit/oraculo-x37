import numpy as np
import shap
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, mean_absolute_error
)
from app.models.model_loader import ModelLoader
from app.core.config import settings

class OracleService:
    def __init__(self, model_type: str = "classification", random_state: int = 42):
        self.model_type = model_type
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = None
        self.model = None
        self.is_trained = False
        self.training_metrics = {}
        self.explainer = None
        self._init_model()

    def _init_model(self):
        if self.model_type == "classification":
            self.model = RandomForestClassifier(
                n_estimators=100, max_depth=15, min_samples_split=5,
                min_samples_leaf=2, random_state=self.random_state, n_jobs=-1
            )
        elif self.model_type == "regression":
            self.model = RandomForestRegressor(
                n_estimators=100, max_depth=15, min_samples_split=5,
                min_samples_leaf=2, random_state=self.random_state, n_jobs=-1
            )
        else:
            raise ValueError("model_type deve ser 'classification' ou 'regression'")

    def train(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Dict[str, float]:
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=self.random_state
        )
        
        self.model.fit(X_train, y_train)
        self.explainer = shap.TreeExplainer(self.model)
        self.is_trained = True
        
        y_pred = self.model.predict(X_test)
        
        if self.model_type == "classification":
            self.training_metrics = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision": float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
                "recall": float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
                "f1_score": float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
                "test_samples": len(y_test),
                "train_samples": len(y_train)
            }
        else:
            self.training_metrics = {
                "mse": float(mean_squared_error(y_test, y_pred)),
                "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
                "mae": float(mean_absolute_error(y_test, y_pred)),
                "r2_score": float(r2_score(y_test, y_pred)),
                "test_samples": len(y_test),
                "train_samples": len(y_train)
            }
        return self.training_metrics

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            raise RuntimeError("Modelo não treinado.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model_type != "classification":
            raise ValueError("Disponível apenas para classificação.")
        if not self.is_trained:
            raise RuntimeError("Modelo não treinado.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)

    def explain_prediction(self, X: np.ndarray, sample_idx: int = 0) -> Dict[str, Any]:
        if not self.is_trained:
            raise RuntimeError("Modelo não treinado.")
        
        X_scaled = self.scaler.transform(X)
        sample = X_scaled[sample_idx:sample_idx+1]
        prediction = self.model.predict(sample)[0]
        
        if self.model_type == "classification":
            probabilities = self.model.predict_proba(sample)[0]
            confidence = float(np.max(probabilities))
            shap_values = self.explainer.shap_values(sample)
            # SHAP 0.45+ retorna array (samples, features, classes) ou similar
            if isinstance(shap_values, list):
                # Caso antigo ou específico
                current_shap = shap_values[int(prediction)][0]
            elif len(shap_values.shape) == 3:
                # (samples, features, classes)
                current_shap = shap_values[0, :, int(prediction)]
            else:
                # (samples, features) para binário ou regressão
                current_shap = shap_values[0]
        else:
            confidence = None
            current_shap = self.explainer.shap_values(sample)[0]
        
        feature_names = self.feature_names or [f"feature_{i}" for i in range(X.shape[1])]
        
        top_impact = {}
        for i, name in enumerate(feature_names):
            top_impact[name] = {
                "shap_value": float(current_shap[i]),
                "feature_value": float(X_scaled[sample_idx, i])
            }
        
        sorted_features = sorted(
            top_impact.items(), key=lambda x: abs(x[1]["shap_value"]), reverse=True
        )[:5]
        
        if isinstance(self.explainer.expected_value, (list, np.ndarray)):
            base_val = float(self.explainer.expected_value[int(prediction)])
        else:
            base_val = float(self.explainer.expected_value)

        return {
            "prediction": int(prediction) if self.model_type == "classification" else float(prediction),
            "confidence": confidence,
            "top_impact_features": dict(sorted_features),
            "base_value": base_val,
            "model_type": self.model_type
        }

    def get_feature_importance(self, top_n: int = 10) -> Dict[str, float]:
        if not self.is_trained:
            raise RuntimeError("Modelo não treinado.")
        importances = self.model.feature_importances_
        feature_names = self.feature_names or [f"feature_{i}" for i in range(len(importances))]
        sorted_idx = np.argsort(importances)[::-1][:top_n]
        return {feature_names[i]: float(importances[i]) for i in sorted_idx}

    def save(self, filepath: str):
        data = {
            "model": self.model, "scaler": self.scaler, "model_type": self.model_type,
            "feature_names": self.feature_names, "training_metrics": self.training_metrics,
            "explainer": self.explainer
        }
        ModelLoader.save_model(data, filepath)

    def load(self, filepath: str):
        data = ModelLoader.load_model(filepath)
        if data:
            self.model = data["model"]
            self.scaler = data["scaler"]
            self.model_type = data["model_type"]
            self.feature_names = data["feature_names"]
            self.training_metrics = data["training_metrics"]
            self.explainer = data.get("explainer")
            self.is_trained = True
            return True
        return False

def generate_sample_data(n_samples: int = 1000, n_features: int = 10, task: str = "classification"):
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    if task == "classification":
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
    else:
        y = X[:, 0] * 2 + X[:, 1] * 3 - X[:, 2] + np.random.randn(n_samples) * 0.1
    return X, y
