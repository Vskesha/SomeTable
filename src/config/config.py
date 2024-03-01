from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    database_url: str = 'postgresql://postgres:567234@localhost:5432/contacts'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
