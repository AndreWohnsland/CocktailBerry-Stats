from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    atlas_uri: str
    debug: bool = False

    @property
    def database_name(self) -> str:
        return "cocktailberry" + ("_dev" if self.debug else "")


SETTINGS = Settings()
