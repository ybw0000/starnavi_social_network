from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    MAX_USERS: int
    MAX_POSTS_PER_USERS: int
    MAX_LIKES_PER_USER: int

    DEBUG: bool = False

    SERVICE_URL: AnyUrl = AnyUrl("http://localhost:8000")
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
