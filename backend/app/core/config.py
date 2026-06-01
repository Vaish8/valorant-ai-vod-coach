from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Valorant AI VOD Coach"
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "valorant_vod_coach"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres"
        "@localhost:5432/valorant_vod_coach"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()