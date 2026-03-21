from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ShoppingList Python API"
    app_env: Literal["local", "test", "production"] = "local"
    app_debug: bool = False
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    api_v1_prefix: str = "/v1"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/shoppinglist"

    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    cors_allow_origins: list[str] = []
    trusted_hosts: list[str] = ["localhost", "127.0.0.1", "testserver"]
    enable_docs: bool = True

    log_level: str = "INFO"
    idempotency_replay_ttl_minutes: int = 1440
    auth_rate_limit_per_minute: int = 10
    share_link_rate_limit_per_minute: int = 30
    max_request_body_bytes: int = 1048576
    enforce_json_content_type: bool = True

    model_config = SettingsConfigDict(
        env_file=None,
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_allow_origins", "trusted_hosts", mode="before")
    @classmethod
    def parse_csv_lists(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_security_controls(self) -> "Settings":
        if len(self.jwt_secret_key.get_secret_value()) < 32:
            raise ValueError("jwt_secret_key must be at least 32 characters long")

        if self.app_env == "production":
            if self.app_debug:
                raise ValueError("app_debug must be false in production")
            if self.enable_docs:
                raise ValueError("enable_docs must be false in production")
            if not self.cors_allow_origins:
                raise ValueError("cors_allow_origins cannot be empty in production")

        if self.idempotency_replay_ttl_minutes <= 0:
            raise ValueError("idempotency_replay_ttl_minutes must be greater than 0")

        if self.auth_rate_limit_per_minute <= 0:
            raise ValueError("auth_rate_limit_per_minute must be greater than 0")

        if self.share_link_rate_limit_per_minute <= 0:
            raise ValueError("share_link_rate_limit_per_minute must be greater than 0")

        if self.max_request_body_bytes <= 0:
            raise ValueError("max_request_body_bytes must be greater than 0")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
