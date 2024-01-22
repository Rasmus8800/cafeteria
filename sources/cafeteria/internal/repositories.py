import collections.abc
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from cafeteria.internal.bases import CRUDRepository
from cafeteria.internal.models import Dish, Menu, Submenu

__all__ = ["DishRepository", "MenuRepository", "SubmenuRepository"]


class DishRepository(CRUDRepository[uuid.UUID, Dish]):
    """Репозиторий блюд."""

    def __init__(self, session_callable: collections.abc.Callable[..., AsyncSession]) -> None:
        """Инициализирует репозиторий блюд.

        :param session_callable: Функция, которая возвращает сессию в базе данных.
        """
        super().__init__(entity_class=Dish, session_callable=session_callable)


class MenuRepository(CRUDRepository[uuid.UUID, Menu]):
    """Репозиторий меню."""

    def __init__(self, session_callable: collections.abc.Callable[..., AsyncSession]) -> None:
        """Инициализирует репозиторий меню.

        :param session_callable: Функция, которая возвращает сессию в базе данных.
        """
        super().__init__(entity_class=Menu, session_callable=session_callable)


class SubmenuRepository(CRUDRepository[uuid.UUID, Submenu]):
    """Репозиторий подменю."""

    def __init__(self, session_callable: collections.abc.Callable[..., AsyncSession]) -> None:
        """Инициализирует репозиторий подменю.

        :param session_callable: Функция, которая возвращает сессию в базе данных.
        """
        super().__init__(entity_class=Submenu, session_callable=session_callable)
