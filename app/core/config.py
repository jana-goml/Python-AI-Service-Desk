from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    AWS_DEMO_MODE: bool
    DATABASE_READY: bool
    BEDROCK_MODEL_ID: str

    class Config:
        env_file = ".env"
        
settings = Settings()