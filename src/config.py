from typing import Annotated, Literal, Union

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsEnv(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"), extra="ignore"
    )


class PostgresSettings(BaseSettingsEnv):
    engine: Literal["postgres"]
    user: str
    password: str
    host: str
    port: int
    db_name: str = Field(alias="db")
    model_config = SettingsConfigDict(env_prefix="postgres_")

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


class SQLiteSettings(BaseSettingsEnv):
    engine: Literal["sqlite"]
    dsn: str = "sqlite:///./db.sqlite3"


class JWTSettings(BaseSettingsEnv):
    secret_key: str = Field(default="secret")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    model_config = SettingsConfigDict(env_prefix="jwt_")


class Settings(BaseSettingsEnv):
    debug: bool = False
    db: Annotated[
        Union[SQLiteSettings, PostgresSettings], Field(discriminator="engine")
    ]
    jwt: JWTSettings = JWTSettings()
    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings()
