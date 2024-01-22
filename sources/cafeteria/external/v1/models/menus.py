import uuid

import pydantic

__all__ = [
    "CreateMenuRequest",
    "CorrectMenuRequest",
    "MenuResponse",
]


class CreateMenuRequest(pydantic.BaseModel):
    """Создаваемое меню."""

    title: str = pydantic.Field(description="Menu title.", max_length=64)
    """Название меню."""
    description: str = pydantic.Field(description="Menu description.", max_length=256)
    """Описание меню."""


class CorrectMenuRequest(pydantic.BaseModel):
    """Изменение меню."""

    title: str = pydantic.Field(description="Corrected menu title.", max_length=64)
    """Название меню."""
    description: str = pydantic.Field(description="Corrected menu description.", max_length=256)
    """Описание меню."""


class MenuResponse(pydantic.BaseModel):
    """Меню."""

    id: uuid.UUID = pydantic.Field(description="Menu identifier.")
    """Идентификатор меню."""
    title: str = pydantic.Field(description="Menu title.", max_length=64)
    """Название меню."""
    description: str = pydantic.Field(description="Menu description.", max_length=256)
    """Описание меню."""
    dishes_count: int = pydantic.Field(description="Dishes counter.")
    """Количество блюд в меню."""
    submenus_count: int = pydantic.Field(description="Submenus counter.")
    """Количество подменю в меню."""
