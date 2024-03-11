from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    database_url: str
