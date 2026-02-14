"""
Demo do Oráculo X-37 - IA Preditiva Offline
Este script simula o uso do Oráculo X-37 em um ambiente interativo.
"""

from oracle_model import OracleX37, generate_sample_data
import numpy as np

def run_demo():
    print("--- Iniciando Demo Oráculo X-37 ---")
    
    # 1. Preparação de Dados
    print("\n1. Gerando dados sintéticos...")
    X, y = generate_sample_data(n_samples=1000, n_features=10, task="classification")
    feature_names = [f"Sensor_{i}" for i in range(10)]
    
    # 2. Inicialização e Treinamento
    print("2. Treinando modelo de classificação...")
    oracle = OracleX37(model_type="classification")
    oracle.set_feature_names(feature_names)
    metrics = oracle.train(X, y)
    
    print(f"   Acurácia: {metrics['accuracy']:.2%}")
    print(f"   F1-Score: {metrics['f1_score']:.2%}")
    
    # 3. Inferência e Explicabilidade
    print("\n3. Analisando uma predição específica...")
    sample_idx = 42
    explanation = oracle.explain_prediction(X, sample_idx=sample_idx)
    
    print(f"   Resultado da Predição: {'ALERTA' if explanation['prediction'] == 1 else 'NORMAL'}")
    print(f"   Confiança: {explanation['confidence']:.2%}")
    print("   Top Features que influenciaram o resultado:")
    for feature, info in explanation['top_features'].items():
        print(f"     - {feature}: Valor={info['value']:.2f} (Importância: {info['importance']:.2f})")

    # 4. Importância Global
    print("\n4. Importância Global das Features:")
    global_importance = oracle.get_feature_importance(top_n=3)
    for feat, imp in global_importance.items():
        print(f"   {feat}: {imp:.4f}")

if __name__ == "__main__":
    run_demo()
