import pickle
import os
from typing import Any, Optional
from app.core.config import settings

class ModelLoader:
    @staticmethod
    def load_model(filepath: str) -> Optional[Any]:
        """Carrega um modelo de arquivo pickle."""
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def save_model(model_data: Any, filepath: str) -> None:
        """Salva um modelo em arquivo pickle."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
