
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: str
    # SERVER_NAME: str
    SECRET_KEY: SecretStr
    JWT_SECRET: SecretStr
    ALGORITHM: SecretStr
    model_config = SettingsConfigDict(
        env_file=('.env', 'stack.env'), env_file_encoding='utf-8', extra='ignore'
    )


settings = Settings()
