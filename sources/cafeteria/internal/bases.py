import abc
import collections.abc
import contextlib
import typing
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["Entity", "CRUDRepository"]

K = typing.TypeVar("K")
"""Тип идентификатора сущности."""


class Entity(typing.Generic[K]):
    """Сущность."""

    id: K
    """Идентификатор сущности."""


T = typing.TypeVar("T", bound=Entity)
"""Идентификатор типа."""


class CRUDRepository(abc.ABC, typing.Generic[K, T]):
    """CRUD-репозиторий."""

    def __init__(
        self,
        *,
        entity_class: type[T],
        session_callable: collections.abc.Callable[..., AsyncSession],
    ) -> None:
        """Инициализирует CRUD-репозиторий.

        :param entity_class: Класс сущности.
        :param session_callable: Функция, которая возвращает сессию в базе данных.
        """
        self._entity_class = entity_class
        self.get_session = session_callable

    async def delete(
        self,
        entity: T,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        """Удаляет сущность из репозитория.

        :param entity: Сущность для удаления.
        :param session: Сессия в базе данных или ничего.
        """
        async with self._wrap_session(session) as session:
            await session.delete(entity)

            await session.flush([entity])

    async def find(
        self,
        entity_id: uuid.UUID,
        *,
        session: AsyncSession | None = None,
    ) -> T | None:
        """Возвращает сущность по указанному идентификатору.

        :param entity_id: Идентификатор сущности.
        :param session: Сессия в базе данных или ничего.
        :returns: Сущность с указанным идентификатором.
        """
        statement = select(self._entity_class).filter(self._entity_class.id == entity_id)

        async with self._wrap_session(session) as session:
            result = await session.scalars(statement)

            return result.one_or_none()

    async def find_all(
        self,
        *,
        session: AsyncSession | None = None,
    ) -> collections.abc.Sequence[T]:
        """Возвращает все сущности из репозитория.

        :param session: Сессия в базе данных или ничего.
        :returns: Все сущности из репозитория.
        """
        statement = select(self._entity_class)

        async with self._wrap_session(session) as session:
            result = await session.scalars(statement)

            return result.all()

    async def save(
        self,
        entity: Entity,
        *,
        session: AsyncSession | None = None,
    ) -> T:
        """Сохраняет сущность в репозиторий.

        :param entity: Сущность для сохранения.
        :param session: Сессия в базе данных или ничего.
        :returns: Сохраненная сущность.
        """
        async with self._wrap_session(session) as session:
            session.add(entity)

            await session.flush([entity])
            await session.refresh(entity)

            return entity

    @contextlib.asynccontextmanager
    async def _wrap_session(
        self,
        session: AsyncSession | None,
    ) -> collections.abc.AsyncIterator[AsyncSession]:
        """Оборачивает сессию, если это требуется.

        :param session: Сессия для оборачивания или ничего.
        :returns: Обернутая сессия.
        """
        if not session:
            async with self.get_session() as wrapped_session:
                yield wrapped_session
        else:
            yield session
