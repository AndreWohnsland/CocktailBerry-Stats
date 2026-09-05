from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # the app runs from the repo root, the frontend/.env entries win over a root .env
    model_config = SettingsConfigDict(env_file=(".env", "frontend/.env"))

    backend_url: str = "http://127.0.0.1:8000/api/v1"
    debug: bool = False


SETTINGS = Settings()
