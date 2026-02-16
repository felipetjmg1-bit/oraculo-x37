import argparse
import sys
import os

# Adicionar o diretório raiz ao path para permitir imports da 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.oracle_service import OracleService, generate_sample_data
from app.core.config import settings

def main():
    parser = argparse.ArgumentParser(description="Treinar modelos do Oráculo X-37")
    parser.add_argument("--type", type=str, choices=["classification", "regression", "both"], 
                        default="both", help="Tipo de modelo a treinar")
    parser.add_argument("--samples", type=int, default=1000, help="Número de amostras")
    parser.add_argument("--features", type=int, default=10, help="Número de features")
    parser.add_argument("--output_clf", type=str, default=settings.DEFAULT_CLF_MODEL_PATH)
    parser.add_argument("--output_reg", type=str, default=settings.DEFAULT_REG_MODEL_PATH)
    
    args = parser.parse_args()
    
    if args.type in ["classification", "both"]:
        print(f"Treinando modelo de classificação ({args.samples} amostras)...")
        service = OracleService(model_type="classification")
        X, y = generate_sample_data(args.samples, args.features, task="classification")
        service.feature_names = [f"Feature_{i}" for i in range(args.features)]
        metrics = service.train(X, y)
        service.save(args.output_clf)
        print(f"✅ Classificação: {metrics}")
        
    if args.type in ["regression", "both"]:
        print(f"Treinando modelo de regressão ({args.samples} amostras)...")
        service = OracleService(model_type="regression")
        X, y = generate_sample_data(args.samples, args.features, task="regression")
        service.feature_names = [f"Feature_{i}" for i in range(args.features)]
        metrics = service.train(X, y)
        service.save(args.output_reg)
        print(f"✅ Regressão: {metrics}")

if __name__ == "__main__":
    main()
