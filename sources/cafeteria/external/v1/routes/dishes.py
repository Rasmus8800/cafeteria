import http
import typing
import uuid

from fastapi import APIRouter, Body, Depends, Path

from cafeteria.external.dependencies import get_cafeteria_service
from cafeteria.external.v1.models.dishes import (
    AddDishToMenuSubmenuRequest,
    CorrectDishInMenuSubmenuRequest,
    DishInMenuSubmenuResponse,
)
from cafeteria.internal.services import CafeteriaService

__all__ = ["router"]


router = APIRouter()


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    status_code=http.HTTPStatus.OK,
    summary="Get dishes",
    description="Get dishes in the menu submenu.",
    response_model=list[DishInMenuSubmenuResponse],
)
async def get_dishes(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> list[DishInMenuSubmenuResponse]:
    """Получает все блюда из подменю меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Список блюд в подменю меню.
    """
    dishes = await cafeteria_service.get_dishes_in_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    return [DishInMenuSubmenuResponse(**dish) for dish in dishes]


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=http.HTTPStatus.OK,
    summary="Get dish",
    description="Get dish in the menu submenu.",
    response_model=DishInMenuSubmenuResponse,
)
async def get_dish(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    dish_id: typing.Annotated[
        uuid.UUID,
        Path(description="Dish identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> DishInMenuSubmenuResponse:
    """Получает блюдо из подменю меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Блюдо в подменю меню.
    """
    dish = await cafeteria_service.get_dish_in_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )

    return DishInMenuSubmenuResponse(**dish)


@router.post(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    status_code=http.HTTPStatus.CREATED,
    summary="Add dish",
    description="Add the dish to the menu submenu.",
    response_model=DishInMenuSubmenuResponse,
)
async def add_dish(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    dish_to_add: typing.Annotated[
        AddDishToMenuSubmenuRequest,
        Body(description="Dish to add"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> DishInMenuSubmenuResponse:
    """Добавляет блюдо в подменю меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_to_add: Блюдо для добавления.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Добавленное блюдо в подменю меню.
    """
    added_dish = await cafeteria_service.add_dish_to_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title=dish_to_add.title,
        description=dish_to_add.description,
        price=dish_to_add.price,
    )

    return DishInMenuSubmenuResponse(**added_dish)


@router.patch(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=http.HTTPStatus.OK,
    summary="Correct dish",
    description="Correct dish in the menu submenu.",
    response_model=DishInMenuSubmenuResponse,
)
async def correct_dish(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    dish_id: typing.Annotated[
        uuid.UUID,
        Path(description="Dish identifier"),
    ],
    dish_to_correct: typing.Annotated[
        CorrectDishInMenuSubmenuRequest,
        Body(description="Dish to correct"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> DishInMenuSubmenuResponse:
    """Корректирует блюдо в подменю меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param dish_to_correct: Блюдо для корректировки.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Скорректированное блюдо в подменю меню.
    """
    corrected_dish = await cafeteria_service.correct_dish_in_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        corrected_title=dish_to_correct.title,
        corrected_description=dish_to_correct.description,
        corrected_price=dish_to_correct.price,
    )

    return DishInMenuSubmenuResponse(**corrected_dish)


@router.delete(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=http.HTTPStatus.OK,
    summary="Remove dish",
    description="Remove dish from the menu submenu.",
    response_model=None,
)
async def remove_dish(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    dish_id: typing.Annotated[
        uuid.UUID,
        Path(description="Dish identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> DishInMenuSubmenuResponse:
    """Удаляет блюдо в подменю меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Удаленное блюдо в подменю меню.
    """
    dish = await cafeteria_service.remove_dish_from_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )

    return DishInMenuSubmenuResponse(**dish)
