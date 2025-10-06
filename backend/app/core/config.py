from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "dkcopy"
    APP_ENV: str = "development" 
    LOG_LEVEL: str = "INFO" # shows normal informational logs!
    OPEN_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5"  # or what you’re actually using
    LLM_PROVIDER: str = "fake"   # "openai" | "fake" | "fake:too_long" | "fake:missing_cta"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    PORT: int = 8000


    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()