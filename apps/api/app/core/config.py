from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tourism.db"
    api_secret_key: str = "dev-secret"
    api_rate_limit: str = "120/minute"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
