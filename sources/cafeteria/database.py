from functools import cached_property

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from cafeteria.settings import DatabaseSettings

__all__ = ["Database", "DatabaseEntity"]


class DatabaseEntity(AsyncAttrs, DeclarativeBase):
    """Сущность базы данных."""


class Database:
    """База данных."""

    def __init__(self, settings: DatabaseSettings) -> None:
        """Инициализация базы данных.

        :param settings: Настройки базы данных.
        """
        self._settings = settings

    @cached_property
    def engine(self) -> AsyncEngine:
        """Движок базы данных."""
        url = URL.create(
            drivername=self._settings.driver,
            username=self._settings.username,
            password=self._settings.password,
            host=self._settings.host,
            port=self._settings.port,
            database=self._settings.database,
        )

        return create_async_engine(
            url=url,
            echo=True,
            pool_pre_ping=True,
        )

    @cached_property
    def session_callable(self) -> async_sessionmaker[AsyncSession]:
        """Фабрика сессий."""
        return async_sessionmaker(
            self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def create_tables(self) -> None:
        """Создает таблицы."""

        async with self.engine.begin() as connection:
            await connection.run_sync(DatabaseEntity.metadata.create_all)
