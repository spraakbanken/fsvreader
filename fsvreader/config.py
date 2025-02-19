from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AppSettings(BaseModel):
    base_url: str | None = None
    root_path: str = ""
    template_directory: str = "templates"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
