from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "dkcopy"
    APP_ENV: str = "development"
    
    # LLM Settings
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-5-20250929"  # Latest Sonnet
    USE_FAKE_LLM: bool = False  # Set to True for testing without API calls
    
    # API Settings
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()