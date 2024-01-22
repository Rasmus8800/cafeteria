import uuid

__all__ = [
    "DishNotFoundError",
    "MenuNotFoundError",
    "SubmenuNotFoundError",
    "SubmenuNotIncludedInMenuError",
]


class DishNotFoundError(Exception):
    """Блюдо не найдено."""

    def __init__(self, dish_id: uuid.UUID):
        super().__init__(f"Dish with id {dish_id} not found!")


class MenuNotFoundError(Exception):
    """Меню не найдено."""

    def __init__(self, menu_id: uuid.UUID):
        super().__init__(f"Menu with id {menu_id} not found!")


class SubmenuNotFoundError(Exception):
    """Подменю не найдено."""

    def __init__(self, submenu_id: uuid.UUID):
        super().__init__(f"Submenu with id {submenu_id} not found!")


class SubmenuNotIncludedInMenuError(Exception):
    """Подменю не включено в меню."""

    def __init__(self, menu_id: uuid.UUID, submenu_id: uuid.UUID):
        super().__init__(f"Submenu with id {submenu_id} is not included in menu with id {menu_id}!")
