from pydantic import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):
    REDIS_HOST: str = Field(env="REDIS_HOST", default="localhost")
    REDIS_PORT: int = Field(env="REDIS_PORT", default=6379)
    REDIS_PWD: str = Field(env="REDIS_PWD", default="")
    REDIS_USER: str = Field(env="REDIS_USER", default="default")
    REDIS_DATABASE: int = Field(env="REDIS_DB", default=8)
    REDIS_DB_QUEUE_CHANNEL: str = Field(
        env="REDIS_DB_QUEUE_CHANNEL", default="socketio_channel_v1"
    )

    @property
    def dsn(self):
        return (
            f"redis://{self.REDIS_USER}:"
            f"{self.REDIS_PWD}@"
            f"{self.REDIS_HOST}:"
            f"{self.REDIS_PORT}/"
            f"{self.REDIS_DATABASE}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class SecuritySettings(BaseSettings):
    JWT_SECRET: str = Field(env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(env="JWT_ALGORITHM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ServicesSettings(BaseSettings):
    AUTH: str = Field(env="API_AUTH")
    CORE: str = Field(env="API_CORE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


redis_settings = RedisSettings()
services_settings = ServicesSettings()
