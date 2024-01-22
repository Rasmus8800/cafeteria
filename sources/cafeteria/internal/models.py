from __future__ import annotations

import decimal
import uuid

from sqlalchemy import UUID, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cafeteria.database import DatabaseEntity
from cafeteria.internal.bases import Entity

__all__ = ["Dish", "Menu", "Submenu"]


class Dish(DatabaseEntity, Entity):
    """Блюдо."""

    __tablename__ = "dishes"

    id: Mapped[uuid.UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    """Идентификатор блюда."""
    title: Mapped[str] = mapped_column(
        "title",
        String(),
        nullable=False,
    )
    """Название блюда."""
    description: Mapped[str] = mapped_column(
        "description",
        String(),
        nullable=False,
    )
    """Описание блюда."""
    price: Mapped[decimal.Decimal] = mapped_column(
        "price",
        Numeric(precision=12, scale=2),
        nullable=False,
    )
    """Цена блюда."""
    submenu_id: Mapped[uuid.UUID] = mapped_column(
        "submenu_id",
        UUID(as_uuid=True),
        ForeignKey("submenus.id", ondelete="CASCADE"),
        nullable=False,
    )
    """Идентификатор подменю."""
    submenu: Mapped[Submenu] = relationship(
        "Submenu",
        back_populates="dishes",
    )
    """Список подменю."""


class Menu(DatabaseEntity, Entity):
    """Меню."""

    __tablename__ = "menus"

    id: Mapped[uuid.UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    """Идентификатор меню."""
    title: Mapped[str] = mapped_column(
        "title",
        String(),
        nullable=False,
    )
    """Название меню."""
    description: Mapped[str] = mapped_column(
        "description",
        String(),
        nullable=False,
    )
    """Описание меню."""
    submenus: Mapped[list[Submenu]] = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete",
        lazy="selectin",
    )
    """Список подменю."""


class Submenu(DatabaseEntity, Entity):
    """Подменю."""

    __tablename__ = "submenus"

    id: Mapped[uuid.UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    """Идентификатор подменю."""
    title: Mapped[str] = mapped_column(
        "title",
        String(),
        nullable=False,
    )
    """Название подменю."""
    description: Mapped[str] = mapped_column(
        "description",
        String(),
        nullable=False,
    )
    """Описание подменю."""
    menu_id: Mapped[uuid.UUID] = mapped_column(
        "menu_id",
        UUID(as_uuid=True),
        ForeignKey("menus.id", ondelete="CASCADE"),
        nullable=False,
    )
    """Идентификатор меню."""
    dishes: Mapped[list[Dish]] = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete",
        lazy="selectin",
    )
    """Список блюд."""
    menu: Mapped[Menu] = relationship(
        "Menu",
        back_populates="submenus",
    )
    """Меню."""
