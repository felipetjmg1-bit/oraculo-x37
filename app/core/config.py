import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    PROJECT_NAME: str = "Oráculo X-37"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # ML Config
    MODELS_DIR: Path = BASE_DIR / "models"
    DEFAULT_CLF_MODEL_PATH: str = os.getenv("CLF_MODEL_PATH", str(MODELS_DIR / "oracle_clf_model.pkl"))
    DEFAULT_REG_MODEL_PATH: str = os.getenv("REG_MODEL_PATH", str(MODELS_DIR / "oracle_reg_model.pkl"))
    
    # Server Config
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
