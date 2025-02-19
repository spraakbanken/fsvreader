from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    base_url: str | None = None
    root_path: str = ""
    template_directory: str = "templates"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="FSVREADER__",
    )
