from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str 
    API_VERSION: str 
    DEBUG: bool 
    DATABASE_URL: str 
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    AWS_ACCESS_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str] 
    AWS_REGION_NAME: str 
    AWS_DEMO_MODE: bool 
    DATABASE_READY: bool 
    BEDROCK_MODEL_ID: Optional[str] 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()