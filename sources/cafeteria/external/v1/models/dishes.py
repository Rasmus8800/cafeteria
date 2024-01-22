import decimal
import uuid

import pydantic

__all__ = [
    "AddDishToMenuSubmenuRequest",
    "CorrectDishInMenuSubmenuRequest",
    "DishInMenuSubmenuResponse",
]


class AddDishToMenuSubmenuRequest(pydantic.BaseModel):
    """Запрос добавления блюда в меню подменю."""

    title: str = pydantic.Field(description="Dish title", max_length=64)
    """Название блюда."""
    description: str = pydantic.Field(description="Dish description", max_length=256)
    """Описание блюда."""
    price: decimal.Decimal = pydantic.Field(decimal_places=2, description="Dish price")
    """Цена блюда."""


class CorrectDishInMenuSubmenuRequest(pydantic.BaseModel):
    """Запрос изменения блюда в меню подменю."""

    title: str = pydantic.Field(description="Corrected dish title", max_length=64)
    """Название блюда."""
    description: str = pydantic.Field(description="Corrected dish description", max_length=256)
    """Описание блюда."""
    price: decimal.Decimal = pydantic.Field(decimal_places=2, description="Corrected dish price")
    """Цена блюда."""


class DishInMenuSubmenuResponse(pydantic.BaseModel):
    """Модель ответа блюдо в подменю меню."""

    id: uuid.UUID
    """Идентификатор блюда."""
    title: str = pydantic.Field(description="Dish title", max_length=64)
    """Название блюда."""
    description: str = pydantic.Field(description="Dish description", max_length=256)
    """Описание блюда."""
    price: decimal.Decimal = pydantic.Field(decimal_places=2, description="Dish price")
    """Цена блюда."""
