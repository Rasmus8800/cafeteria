import http
import typing
import uuid

from fastapi import APIRouter, Body, Depends, Path

from cafeteria.external.dependencies import get_cafeteria_service
from cafeteria.external.v1.models.submenus import (
    CorrectMenuSubmenuRequest,
    CreateMenuSubmenuRequest,
    MenuSubmenuResponse,
)
from cafeteria.internal.services import CafeteriaService

__all__ = ["router"]


router = APIRouter()


@router.get(
    path="/menus/{menu_id}/submenus",
    status_code=http.HTTPStatus.OK,
    summary="Get submenus",
    description="Get submenus in the menu.",
    response_model=list[MenuSubmenuResponse],
)
async def get_submenus(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> list[MenuSubmenuResponse]:
    """Получает все подменю в меню.

    :param menu_id: Идентификатор меню.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Список подменю в меню.
    """
    submenus = await cafeteria_service.get_menu_submenus(
        menu_id=menu_id,
    )

    return [MenuSubmenuResponse(**submenu) for submenu in submenus]


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Get submenu",
    description="Get submenu in the menu.",
    response_model=MenuSubmenuResponse,
)
async def get_submenu(
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
) -> MenuSubmenuResponse:
    """Получает конкретное подменю в меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Подменю в меню.
    """
    submenu = await cafeteria_service.get_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    return MenuSubmenuResponse(**submenu)


@router.post(
    path="/menus/{menu_id}/submenus",
    status_code=http.HTTPStatus.CREATED,
    summary="Create submenu",
    description="Create submenu in the menu.",
    response_model=MenuSubmenuResponse,
)
async def create_submenu(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_to_create: typing.Annotated[
        CreateMenuSubmenuRequest,
        Body(description="Submenu to create."),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuSubmenuResponse:
    """Создает подменю в меню.

    :param menu_id: Идентификатор меню.
    :param submenu_to_create: Подменю для создания.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Созданное подменю в меню.
    """
    submenu = await cafeteria_service.create_menu_submenu(
        menu_id=menu_id,
        title=submenu_to_create.title,
        description=submenu_to_create.description,
    )

    return MenuSubmenuResponse(**submenu)


@router.patch(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Correct submenu",
    description="Correct submenu in the menu.",
    response_model=MenuSubmenuResponse,
)
async def correct_submenu(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    submenu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Submenu identifier"),
    ],
    submenu_to_correct: typing.Annotated[
        CorrectMenuSubmenuRequest,
        Body(description="Submenu to correct."),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuSubmenuResponse:
    """Корректирует подменю в меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param submenu_to_correct: Подменю для корректировки.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Скорректированное подменю в меню.
    """
    submenu = await cafeteria_service.correct_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        corrected_title=submenu_to_correct.title,
        corrected_description=submenu_to_correct.description,
    )

    return MenuSubmenuResponse(**submenu)


@router.delete(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Delete submenu",
    description="Delete submenu in the menu.",
    response_model=None,
)
async def delete_submenu(
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
) -> MenuSubmenuResponse:
    """Удаляет подменю в меню.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Удаленное подменю в меню.
    """
    submenu = await cafeteria_service.delete_menu_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )

    return MenuSubmenuResponse(**submenu)
