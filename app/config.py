
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME : str
    GEMINI_API_KEY: str
    MAX_RESULTS: int = 10
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()