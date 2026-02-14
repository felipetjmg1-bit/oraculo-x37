"""
Oráculo X-37: MVP de IA Preditiva Offline com Explicabilidade

Este módulo implementa um modelo de machine learning preditivo com explicabilidade (XAI)
usando SHAP para interpretação das previsões.
"""

import json
import pickle
import numpy as np
import pandas as pd
import shap
from pathlib import Path
from typing import Dict, List, Tuple, Any

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


class OracleX37:
    """
    Oráculo X-37: Sistema de IA Preditiva Offline com Explicabilidade.
    
    Características principais:
    - Funciona completamente offline
    - Oferece explicabilidade das previsões
    - Modo seguro de operação
    - Suporta classificação e regressão
    """

    def __init__(self, model_type: str = "classification", random_state: int = 42):
        """
        Inicializa o Oráculo X-37.
        
        Args:
            model_type: "classification" ou "regression"
            random_state: Seed para reprodutibilidade
        """
        self.model_type = model_type
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = None
        self.model = None
        self.is_trained = False
        self.training_metrics = {}
        self.explainer = None

        if model_type == "classification":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1
            )
        elif model_type == "regression":
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1
            )
        else:
            raise ValueError("model_type deve ser 'classification' ou 'regression'")

    def train(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Dict[str, float]:
        """
        Treina o modelo com os dados fornecidos.
        
        Args:
            X: Array de features (n_samples, n_features)
            y: Array de targets (n_samples,)
            test_size: Proporção de dados para teste
            
        Returns:
            Dicionário com métricas de desempenho
        """
        # Normalizar os dados
        X_scaled = self.scaler.fit_transform(X)
        
        # Dividir em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=self.random_state
        )
        
        # Treinar o modelo
        self.model.fit(X_train, y_train)
        
        # Inicializar o explicador SHAP
        self.explainer = shap.TreeExplainer(self.model)
        
        self.is_trained = True
        
        # Calcular métricas
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
        """
        Realiza predições com o modelo treinado.
        
        Args:
            X: Array de features
            
        Returns:
            Array com as predições
        """
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Retorna probabilidades das predições (apenas para classificação).
        
        Args:
            X: Array de features
            
        Returns:
            Array com as probabilidades
        """
        if self.model_type != "classification":
            raise ValueError("predict_proba está disponível apenas para classificação")
        
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)

    def get_feature_importance(self, top_n: int = 10) -> Dict[str, float]:
        """
        Retorna a importância das features do modelo.
        
        Args:
            top_n: Número de top features a retornar
            
        Returns:
            Dicionário com importância das features
        """
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        importances = self.model.feature_importances_
        
        if self.feature_names is None:
            feature_names = [f"feature_{i}" for i in range(len(importances))]
        else:
            feature_names = self.feature_names
        
        # Ordenar por importância
        sorted_idx = np.argsort(importances)[::-1][:top_n]
        
        return {
            feature_names[i]: float(importances[i])
            for i in sorted_idx
        }

    def explain_prediction(self, X: np.ndarray, sample_idx: int = 0) -> Dict[str, Any]:
        """
        Explica uma predição específica usando SHAP (Explicabilidade avançada).
        
        Args:
            X: Array de features
            sample_idx: Índice da amostra a explicar
            
        Returns:
            Dicionário com explicação detalhada da predição
        """
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        X_scaled = self.scaler.transform(X)
        sample = X_scaled[sample_idx:sample_idx+1]
        
        prediction = self.model.predict(sample)[0]
        
        if self.model_type == "classification":
            probabilities = self.model.predict_proba(sample)[0]
            confidence = float(np.max(probabilities))
            # Para SHAP em classificação binária, pegamos os valores para a classe predita
            shap_values = self.explainer.shap_values(sample)
            # Se for lista (multiclasse), pega a predição atual, senão pega direto (binário em algumas versões)
            if isinstance(shap_values, list):
                current_shap = shap_values[int(prediction)][0]
            else:
                current_shap = shap_values[0]
        else:
            confidence = None
            current_shap = self.explainer.shap_values(sample)[0]
        
        if self.feature_names is None:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        else:
            feature_names = self.feature_names
        
        # Criar dicionário de impactos SHAP
        shap_explanation = {}
        for i, name in enumerate(feature_names):
            shap_explanation[name] = {
                "shap_value": float(current_shap[i]),
                "feature_value": float(X_scaled[sample_idx, i])
            }
        
        # Ordenar por impacto absoluto
        sorted_features = sorted(
            shap_explanation.items(), 
            key=lambda item: abs(item[1]["shap_value"]), 
            reverse=True
        )[:5]
        
        # Obter valor base
        if isinstance(self.explainer.expected_value, (list, np.ndarray)):
            base_val = float(self.explainer.expected_value[int(prediction)])
        else:
            base_val = float(self.explainer.expected_value)

        explanation = {
            "prediction": int(prediction) if self.model_type == "classification" else float(prediction),
            "confidence": confidence,
            "top_impact_features": dict(sorted_features),
            "base_value": base_val,
            "model_type": self.model_type,
            "method": "SHAP (Lundberg et al.)"
        }
        
        return explanation

    def save_model(self, filepath: str) -> None:
        """
        Salva o modelo treinado em arquivo.
        
        Args:
            filepath: Caminho do arquivo para salvar
        """
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "model_type": self.model_type,
            "feature_names": self.feature_names,
            "training_metrics": self.training_metrics,
            "explainer": self.explainer
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filepath: str) -> None:
        """
        Carrega um modelo treinado de arquivo.
        
        Args:
            filepath: Caminho do arquivo para carregar
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.model_type = model_data["model_type"]
        self.feature_names = model_data["feature_names"]
        self.training_metrics = model_data["training_metrics"]
        self.explainer = model_data.get("explainer")
        self.is_trained = True

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna as métricas de treinamento.
        
        Returns:
            Dicionário com as métricas
        """
        if not self.is_trained:
            raise RuntimeError("Modelo não foi treinado. Execute train() primeiro.")
        
        return self.training_metrics

    def set_feature_names(self, names: List[str]) -> None:
        """
        Define os nomes das features.
        
        Args:
            names: Lista com os nomes das features
        """
        self.feature_names = names


def generate_sample_data(n_samples: int = 1000, n_features: int = 10, 
                         task: str = "classification") -> Tuple[np.ndarray, np.ndarray]:
    """
    Gera dados de exemplo para demonstração.
    
    Args:
        n_samples: Número de amostras
        n_features: Número de features
        task: "classification" ou "regression"
        
    Returns:
        Tupla (X, y) com dados gerados
    """
    np.random.seed(42)
    
    X = np.random.randn(n_samples, n_features)
    
    if task == "classification":
        # Criar um problema de classificação binária
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
    else:
        # Criar um problema de regressão
        y = X[:, 0] * 2 + X[:, 1] * 3 - X[:, 2] + np.random.randn(n_samples) * 0.1
    
    return X, y


if __name__ == "__main__":
    print("=" * 60)
    print("🔮 Oráculo X-37: MVP de IA Preditiva Offline")
    print("=" * 60)
    
    # Exemplo 1: Classificação
    print("\n📊 Exemplo 1: Modelo de Classificação")
    print("-" * 60)
    
    oracle_clf = OracleX37(model_type="classification")
    X_clf, y_clf = generate_sample_data(n_samples=1000, n_features=10, task="classification")
    
    oracle_clf.set_feature_names([f"Feature_{i}" for i in range(X_clf.shape[1])])
    
    metrics_clf = oracle_clf.train(X_clf, y_clf)
    print("\n✅ Modelo treinado com sucesso!")
    print(f"Acurácia: {metrics_clf['accuracy']:.4f}")
    print(f"Precisão: {metrics_clf['precision']:.4f}")
    print(f"Recall: {metrics_clf['recall']:.4f}")
    print(f"F1-Score: {metrics_clf['f1_score']:.4f}")
    
    # Fazer uma predição
    sample_X = X_clf[:1]
    prediction = oracle_clf.predict(sample_X)
    explanation = oracle_clf.explain_prediction(X_clf, sample_idx=0)
    
    print(f"\n🎯 Predição para amostra 0: {prediction[0]}")
    print(f"Confiança: {explanation['confidence']:.4f}")
    print("\nTop Features:")
    for feature, info in explanation['top_features'].items():
        print(f"  - {feature}: importância={info['importance']:.4f}, valor={info['value']:.4f}")
    
    # Importância das features
    print("\n📈 Importância das Features:")
    importances = oracle_clf.get_feature_importance(top_n=5)
    for feature, importance in importances.items():
        print(f"  - {feature}: {importance:.4f}")
    
    # Exemplo 2: Regressão
    print("\n\n📊 Exemplo 2: Modelo de Regressão")
    print("-" * 60)
    
    oracle_reg = OracleX37(model_type="regression")
    X_reg, y_reg = generate_sample_data(n_samples=1000, n_features=10, task="regression")
    
    oracle_reg.set_feature_names([f"Feature_{i}" for i in range(X_reg.shape[1])])
    
    metrics_reg = oracle_reg.train(X_reg, y_reg)
    print("\n✅ Modelo treinado com sucesso!")
    print(f"R² Score: {metrics_reg['r2_score']:.4f}")
    print(f"RMSE: {metrics_reg['rmse']:.4f}")
    print(f"MAE: {metrics_reg['mae']:.4f}")
    
    # Fazer uma predição
    prediction_reg = oracle_reg.predict(X_reg[:1])
    explanation_reg = oracle_reg.explain_prediction(X_reg, sample_idx=0)
    
    print(f"\n🎯 Predição para amostra 0: {prediction_reg[0]:.4f}")
    print("\nTop Features:")
    for feature, info in explanation_reg['top_features'].items():
        print(f"  - {feature}: importância={info['importance']:.4f}, valor={info['value']:.4f}")
    
    # Salvar modelo
    print("\n\n💾 Salvando modelos...")
    oracle_clf.save_model("oracle_clf_model.pkl")
    oracle_reg.save_model("oracle_reg_model.pkl")
    print("✅ Modelos salvos com sucesso!")
    
    print("\n" + "=" * 60)
    print("✨ Demonstração concluída com sucesso!")
    print("=" * 60)
