import typing

from fastapi import Depends, FastAPI, Request

from cafeteria.database import Database
from cafeteria.internal.repositories import (
    DishRepository,
    MenuRepository,
    SubmenuRepository,
)
from cafeteria.internal.services import CafeteriaService

__all__ = [
    "get_app",
    "get_database",
    "get_dish_repository",
    "get_submenu_repository",
    "get_menus_repository",
    "get_cafeteria_service",
]


async def get_app(request: Request) -> FastAPI:
    """Получает текущего приложения FastAPI.

    :param request: Запрос к текущему приложению FastAPI.
    :returns: Текущее приложения FastAPI.
    """
    return request.app


async def get_database(
    app: typing.Annotated[
        FastAPI,
        Depends(dependency=get_app),
    ]
) -> Database:
    """Получает базу данных.

    :param app: Текущее приложение, содержащее базу данных.
    :returns: Базу данных.
    """
    return app.state.database


async def get_dish_repository(
    database: typing.Annotated[
        Database,
        Depends(dependency=get_database),
    ]
) -> DishRepository:
    """Получает репозиторий блюд.

    :param database: База данных.
    :returns: Репозиторий блюд.
    """
    return DishRepository(session_callable=database.session_callable)


async def get_submenu_repository(
    database: typing.Annotated[
        Database,
        Depends(dependency=get_database),
    ]
) -> SubmenuRepository:
    """Получает репозиторий подменю.

    :param database: База данных.
    :returns: Репозиторий подменю.
    """
    return SubmenuRepository(session_callable=database.session_callable)


async def get_menus_repository(
    database: typing.Annotated[
        Database,
        Depends(dependency=get_database),
    ]
) -> MenuRepository:
    """Получает репозиторий меню.

    :param database: База данных.
    :returns: Репозиторий меню.
    """
    return MenuRepository(session_callable=database.session_callable)


async def get_cafeteria_service(
    dish_repository: typing.Annotated[
        DishRepository,
        Depends(dependency=get_dish_repository),
    ],
    submenu_repository: typing.Annotated[
        SubmenuRepository,
        Depends(dependency=get_submenu_repository),
    ],
    menu_repository: typing.Annotated[
        MenuRepository,
        Depends(dependency=get_menus_repository),
    ],
) -> CafeteriaService:
    """Получает сервис кафетерии.

    :param dish_repository: Репозиторий блюд.
    :param submenu_repository: Репозиторий подменю.
    :param menu_repository: Репозиторий меню.
    :returns: Сервис кафетерии.
    """
    return CafeteriaService(
        dish_repository=dish_repository,
        submenu_repository=submenu_repository,
        menu_repository=menu_repository,
    )
