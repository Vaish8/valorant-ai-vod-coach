from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Valorant AI VOD Coach"
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()