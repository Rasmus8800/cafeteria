import http
import typing
import uuid

from fastapi import APIRouter, Body, Depends, Path

from cafeteria.external.dependencies import get_cafeteria_service
from cafeteria.external.v1.models.menus import (
    CorrectMenuRequest,
    CreateMenuRequest,
    MenuResponse,
)
from cafeteria.internal.services import CafeteriaService

__all__ = ["router"]


router = APIRouter()


@router.get(
    path="/menus",
    status_code=http.HTTPStatus.OK,
    summary="Get menus",
    description="Get menus.",
    response_model=list[MenuResponse],
)
async def get_menus(
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> list[MenuResponse]:
    """Получает все меню.

    :param cafeteria_service: Сервис кафетерии.
    :returns: Список меню.
    """
    menus = await cafeteria_service.get_menus()

    return [MenuResponse(**menu) for menu in menus]


@router.get(
    path="/menus/{menu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Get menu",
    description="Get menu.",
    response_model=MenuResponse,
)
async def get_menu(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuResponse:
    """Получает меню.

    :param menu_id: Идентификатор меню.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Меню.
    """
    menu = await cafeteria_service.get_menu(
        menu_id=menu_id,
    )

    return MenuResponse(**menu)


@router.post(
    path="/menus",
    status_code=http.HTTPStatus.CREATED,
    summary="Create menu",
    description="Create menu.",
    response_model=MenuResponse,
)
async def create_menu(
    menu_to_create: typing.Annotated[
        CreateMenuRequest,
        Body(description="Menu to create."),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuResponse:
    """Создает меню.

    :param menu_to_create: Меню для создания.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Созданное меню.
    """
    menu = await cafeteria_service.create_menu(
        title=menu_to_create.title,
        description=menu_to_create.description,
    )

    return MenuResponse(**menu)


@router.patch(
    path="/menus/{menu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Correct menu",
    description="Correct menu.",
    response_model=MenuResponse,
)
async def correct_menu(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    menu_to_correct: typing.Annotated[
        CorrectMenuRequest,
        Body(description="Menu to correct."),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuResponse:
    """Корректирует меню.

    :param menu_id: Идентификатор меню.
    :param menu_to_correct: Меню для корректировки.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Скорректированное меню.
    """
    menu = await cafeteria_service.correct_menu(
        menu_id=menu_id,
        corrected_title=menu_to_correct.title,
        corrected_description=menu_to_correct.description,
    )

    return MenuResponse(**menu)


@router.delete(
    path="/menus/{menu_id}",
    status_code=http.HTTPStatus.OK,
    summary="Delete menu",
    description="Delete menu.",
    response_model=None,
)
async def delete_menu(
    menu_id: typing.Annotated[
        uuid.UUID,
        Path(description="Menu identifier"),
    ],
    cafeteria_service: typing.Annotated[
        CafeteriaService,
        Depends(dependency=get_cafeteria_service),
    ],
) -> MenuResponse:
    """Удаляет меню.

    :param menu_id: Идентификатор меню.
    :param cafeteria_service: Сервис кафетерии.
    :returns: Удаленное меню.
    """
    menu = await cafeteria_service.delete_menu(menu_id=menu_id)

    return MenuResponse(**menu)
