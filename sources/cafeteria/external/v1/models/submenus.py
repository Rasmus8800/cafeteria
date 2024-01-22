import uuid

import pydantic

__all__ = [
    "CreateMenuSubmenuRequest",
    "CorrectMenuSubmenuRequest",
    "MenuSubmenuResponse",
]


class CreateMenuSubmenuRequest(pydantic.BaseModel):
    """Запрос создания подменю в меню."""

    title: str = pydantic.Field(description="Submenu title.", max_length=64)
    """Название подменю."""
    description: str = pydantic.Field(description="Submenu description.", max_length=256)
    """Описание подменю."""


class CorrectMenuSubmenuRequest(pydantic.BaseModel):
    """Запрос изменения подменю в меню."""

    title: str = pydantic.Field(description="Corrected submenu title.", max_length=64)
    """Название подменю."""
    description: str = pydantic.Field(description="Corrected submenu description.", max_length=256)
    """Описание подменю."""


class MenuSubmenuResponse(pydantic.BaseModel):
    """Подменю меню."""

    id: uuid.UUID = pydantic.Field(description="Submenu identifier.")
    """Идентификатор подменю."""
    title: str = pydantic.Field(description="Submenu title.", max_length=64)
    """Название подменю."""
    description: str = pydantic.Field(description="Submenu description.", max_length=256)
    """Описание подменю."""
    dishes_count: int = pydantic.Field(description="Dishes counter.")
    """Количество блюд в подменю."""
