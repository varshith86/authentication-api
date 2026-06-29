from pydantic_settings import BaseSettings  # pip install pydantic-settings

class Settings(BaseSettings):
    app_name: str="Authentication API"
    app_version: str="1.0.0"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
