from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tourism.db"
    redis_url: str = "redis://localhost:6379/0"
    crawl_delay_seconds: float = 0.5
    crawl_concurrency: int = 4
    respect_robots: bool = True
    s3_bucket: str = "tourism-raw"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
