import collections.abc
import decimal
import uuid

from cafeteria.internal.exceptions import (
    DishNotFoundError,
    MenuNotFoundError,
    SubmenuNotFoundError,
    SubmenuNotIncludedInMenuError,
)
from cafeteria.internal.models import Dish, Menu, Submenu
from cafeteria.internal.repositories import (
    DishRepository,
    MenuRepository,
    SubmenuRepository,
)

__all__ = ["CafeteriaService"]


class CafeteriaService:
    """Сервис кафетерии."""

    def __init__(
        self,
        dish_repository: DishRepository,
        menu_repository: MenuRepository,
        submenu_repository: SubmenuRepository,
    ) -> None:
        """Инициализирует сервис кафетерии.

        :param dish_repository: Репозиторий блюд.
        :param menu_repository: Репозиторий меню.
        :param submenu_repository: Репозиторий подменю.
        """
        self.dish_repository = dish_repository
        self.menu_repository = menu_repository
        self.submenu_repository = submenu_repository

    async def get_dish_in_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Получает блюдо из подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :raises DishNotFoundError: Если блюдо не найдено внутри под
        :returns: Блюдо из подменю меню.
        """
        menu = await self.menu_repository.find(entity_id=menu_id)

        if not menu:
            raise MenuNotFoundError(menu_id=menu_id)

        submenu = await self.submenu_repository.find(entity_id=submenu_id)

        if not submenu:
            raise SubmenuNotFoundError(submenu_id=submenu_id)

        if submenu not in menu.submenus:
            raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

        dish = await self.dish_repository.find(entity_id=dish_id)

        if not dish:
            raise DishNotFoundError(dish_id=dish_id)

        return {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
        }

    async def get_dishes_in_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> collections.abc.Sequence[collections.abc.Mapping[str, object]]:
        """Получает все блюда из подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :returns: Список блюд из подменю меню.
        """
        menu = await self.menu_repository.find(entity_id=menu_id)

        if not menu:
            raise MenuNotFoundError(menu_id=menu_id)

        submenu = await self.submenu_repository.find(entity_id=submenu_id)

        if not submenu:
            # raise SubmenuNotFoundError(submenu_id=submenu_id)
            return []

        if submenu not in menu.submenus:
            raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

        return [
            {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
            for dish in submenu.dishes
        ]

    async def add_dish_to_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        title: str,
        description: str,
        price: decimal.Decimal,
    ) -> collections.abc.Mapping[str, object]:
        """Добавляет блюдо в подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param title: Название блюда.
        :param description: Описание блюда.
        :param price: Цена блюда.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :returns: Список блюд из подменю меню.
        """
        async with self.dish_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.find(entity_id=submenu_id, session=session)

            if not submenu:
                raise SubmenuNotFoundError(submenu_id=submenu_id)

            if submenu not in menu.submenus:
                raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

            dish = await self.dish_repository.save(
                entity=Dish(
                    title=title,
                    description=description,
                    price=price,
                    submenu_id=submenu_id,
                ),
                session=session,
            )

            return {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }

    async def correct_dish_in_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        corrected_title: str | None = None,
        corrected_description: str | None = None,
        corrected_price: decimal.Decimal | None = None,
    ) -> collections.abc.Mapping[str, object]:
        """Корректирует блюдо в подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        :param corrected_title: Измененное название блюда.
        :param corrected_description: Измененное описание блюда.
        :param corrected_price: Измененная цена блюда.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :raises DishNotFoundError: Если блюдо не найдено внутри подменю.
        :returns: Скорректированное блюдо из подменю меню.
        """
        async with self.dish_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.find(entity_id=submenu_id, session=session)

            if not submenu:
                raise SubmenuNotFoundError(submenu_id=submenu_id)

            if submenu not in menu.submenus:
                raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

            dish = await self.dish_repository.find(entity_id=dish_id, session=session)

            if not dish:
                raise DishNotFoundError(dish_id=dish_id)

            dish.title = corrected_title or dish.title
            dish.description = corrected_description or dish.description
            dish.price = corrected_price or dish.price

            dish = await self.dish_repository.save(entity=dish, session=session)

            return {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }

    async def remove_dish_from_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Удаляет блюдо из подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :raises DishNotFoundError: Если блюдо не найдено внутри подменю.
        :returns: Удаленное блюдо из подменю меню.
        """
        async with self.dish_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.find(entity_id=submenu_id, session=session)

            if not submenu:
                raise SubmenuNotFoundError(submenu_id=submenu_id)

            if submenu not in menu.submenus:
                raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

            dish = await self.dish_repository.find(entity_id=dish_id, session=session)

            if not dish:
                raise DishNotFoundError(dish_id=dish_id)

            await self.dish_repository.delete(entity=dish, session=session)

            return {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }

    async def get_menu(
        self,
        menu_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Получает меню.

        :param menu_id: Идентификатор меню.
        :raises MenuNotFoundError: Если меню не найдено.
        :returns: Меню.
        """
        menu = await self.menu_repository.find(entity_id=menu_id)

        if not menu:
            raise MenuNotFoundError(menu_id=menu_id)

        return {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "dishes_count": sum(len(submenu.dishes) for submenu in menu.submenus),
            "submenus_count": len(menu.submenus),
        }

    async def get_menus(
        self,
    ) -> collections.abc.Sequence[collections.abc.Mapping[str, object]]:
        """Получает все меню.

        :returns: Список меню.
        """
        menus = await self.menu_repository.find_all()

        return [
            {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "dishes_count": sum(len(submenu.dishes) for submenu in menu.submenus),
                "submenus_count": len(menu.submenus),
            }
            for menu in menus
        ]

    async def create_menu(
        self,
        title: str,
        description: str,
    ) -> collections.abc.Mapping[str, object]:
        """Создает меню.

        :param title: Название меню.
        :param description: Описание меню.
        :returns: Созданное меню.
        """
        async with self.menu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.save(
                entity=Menu(
                    title=title,
                    description=description,
                ),
                session=session,
            )

            return {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "dishes_count": sum(len(submenu.dishes) for submenu in menu.submenus),
                "submenus_count": len(menu.submenus),
            }

    async def correct_menu(
        self,
        menu_id: uuid.UUID,
        corrected_title: str | None = None,
        corrected_description: str | None = None,
    ) -> collections.abc.Mapping[str, object]:
        """Корректирует меню.

        :param menu_id: Идентификатор меню.
        :param corrected_title: Измененное название меню.
        :param corrected_description: Измененное описание меню.
        :raises MenuNotFoundError: Если меню не найдено.
        :returns: Скорректированное меню.
        """
        async with self.menu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            menu.title = corrected_title or menu.title
            menu.description = corrected_description or menu.description

            menu = await self.menu_repository.save(entity=menu, session=session)

            return {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "dishes_count": sum(len(submenu.dishes) for submenu in menu.submenus),
                "submenus_count": len(menu.submenus),
            }

    async def delete_menu(
        self,
        menu_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Удаляет меню.

        :param menu_id: Идентификатор меню.
        :raises MenuNotFoundError: Если меню не найдено.
        :returns: Удаленное меню.
        """
        async with self.menu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            await self.menu_repository.delete(entity=menu, session=session)

            return {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "dishes_count": sum(len(submenu.dishes) for submenu in menu.submenus),
                "submenus_count": len(menu.submenus),
            }

    async def get_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Получает подменю меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :returns: Подменю меню.
        """
        menu = await self.menu_repository.find(entity_id=menu_id)

        if not menu:
            raise MenuNotFoundError(menu_id=menu_id)

        submenu = await self.submenu_repository.find(entity_id=submenu_id)

        if not submenu:
            raise SubmenuNotFoundError(submenu_id=submenu_id)

        if submenu not in menu.submenus:
            raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

        return {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": len(submenu.dishes),
        }

    async def get_menu_submenus(
        self,
        menu_id: uuid.UUID,
    ) -> collections.abc.Sequence[collections.abc.Mapping[str, object]]:
        """Получает все подменю в меню.

        :param menu_id: Идентификатор меню.
        :raises MenuNotFoundError: Если меню не найдено.
        :returns: Список подменю меню.
        """
        menu = await self.menu_repository.find(entity_id=menu_id)

        if not menu:
            raise MenuNotFoundError(menu_id=menu_id)

        submenus = await self.submenu_repository.find_all()

        return [
            {
                "id": submenu.id,
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": len(submenu.dishes),
            }
            for submenu in submenus
        ]

    async def create_menu_submenu(
        self,
        menu_id: uuid.UUID,
        title: str,
        description: str,
    ) -> collections.abc.Mapping[str, object]:
        """Создает подменю внутри меню.

        :param menu_id: Идентификатор меню.
        :param title: Название подменю.
        :param description: Описание подменю.
        :raises MenuNotFoundError: Если меню не найдено.
        :returns: Созданное подменю внутри меню.
        """
        async with self.submenu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.save(
                entity=Submenu(
                    title=title,
                    description=description,
                    menu_id=menu_id,
                ),
                session=session,
            )

            return {
                "id": submenu.id,
                "title": submenu.title,
                "description": menu.description,
                "dishes_count": len(submenu.dishes),
            }

    async def correct_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        corrected_title: str | None = None,
        corrected_description: str | None = None,
    ) -> collections.abc.Mapping[str, object]:
        """Корректирует подменю внутри меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param corrected_title: Измененное название подменю.
        :param corrected_description: Измененное описание подменю.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :returns: Скорректированное подменю внутри меню.
        """
        async with self.submenu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.find(entity_id=submenu_id, session=session)

            if not submenu:
                raise SubmenuNotFoundError(submenu_id=submenu_id)

            if submenu not in menu.submenus:
                raise SubmenuNotIncludedInMenuError(menu_id=menu_id, submenu_id=submenu_id)

            submenu.title = corrected_title or submenu.title
            submenu.description = corrected_description or submenu.description

            submenu = await self.submenu_repository.save(entity=submenu, session=session)

            return {
                "id": submenu.id,
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": len(submenu.dishes),
            }

    async def delete_menu_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> collections.abc.Mapping[str, object]:
        """Удаляет подменю внутри меню.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :raises MenuNotFoundError: Если меню не найдено.
        :raises SubmenuNotFoundError: Если подменю меню не найдено.
        :raises SubmenuNotIncludedInMenuError: Если подменю не включено в меню.
        :returns: Удаленное подменю внутри меню.
        """
        async with self.submenu_repository.get_session() as session, session.begin():
            menu = await self.menu_repository.find(entity_id=menu_id, session=session)

            if not menu:
                raise MenuNotFoundError(menu_id=menu_id)

            submenu = await self.submenu_repository.find(entity_id=submenu_id, session=session)

            if not submenu:
                raise SubmenuNotFoundError(submenu_id=submenu_id)

            await self.submenu_repository.delete(entity=submenu, session=session)

            return {
                "id": submenu.id,
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": len(submenu.dishes),
            }
