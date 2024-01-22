import pydantic
import pydantic_settings

__all__ = ["DatabaseSettings", "Settings", "settings"]


class DatabaseSettings(pydantic.BaseModel):
    """Настройки базы данных."""

    driver: str = pydantic.Field(default="postgresql+asyncpg")
    """Драйвер."""
    username: str = pydantic.Field(default="postgres")
    """Имя пользователя."""
    password: str = pydantic.Field(default="postgres")
    """Пароль пользователя."""
    host: str = pydantic.Field(default="localhost")
    """Хост."""
    port: int = pydantic.Field(default=5432)
    """Порт."""
    database: str = pydantic.Field(default="postgres")
    """Название базы данных."""


class Settings(pydantic_settings.BaseSettings):
    """Настройки приложения."""

    database: DatabaseSettings = pydantic.Field(default_factory=DatabaseSettings)
    """Настройки базы данных."""


settings = Settings(_env_nested_delimiter="__")
"""Экземпляр настроек приложения."""
