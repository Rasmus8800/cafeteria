import collections.abc
import contextlib
import http

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from loguru import logger

from cafeteria.database import Database
from cafeteria.external import v1
from cafeteria.internal.exceptions import (
    DishNotFoundError,
    MenuNotFoundError,
    SubmenuNotFoundError,
    SubmenuNotIncludedInMenuError,
)
from cafeteria.settings import settings

__all__ = ["app"]


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> collections.abc.AsyncIterator[None]:
    """Жизненный цикл приложения."""

    logger.info(settings.database)

    database = Database(settings=settings.database)

    from cafeteria.internal import (  # noqa: F401 Быстрый фикс для доступности моделей (они не создавались).
        models,
    )

    await database.create_tables()

    app.state.database = database

    yield

    await database.engine.dispose()


app = FastAPI(
    title="Cafeteria",
    summary="Cafeteria API",
    lifespan=lifespan,
)
"""Приложение FastAPI."""


@app.exception_handler(DishNotFoundError)
async def dish_not_found_handler(
    request: Request,
    error: DishNotFoundError,
) -> ORJSONResponse:
    """Обрабатывает ошибку, когда блюдо из подменю не найдено.

    :param request: Текущий запрос.
    :param error: Перехваченная ошибка, когда блюдо из подменю не найдено.
    :returns: Ответ со статусом `404 Not Found` и детали.
    """
    return ORJSONResponse(
        status_code=http.HTTPStatus.NOT_FOUND,
        content={"detail": "dish not found"},
    )


@app.exception_handler(SubmenuNotFoundError)
async def submenu_not_found_handler(
    request: Request,
    error: SubmenuNotFoundError,
) -> ORJSONResponse:
    """Обрабатывает ошибку, когда подменю не найдено в меню.

    :param request: Текущий запрос.
    :param error: Перехваченная ошибка, когда подменю не найдено в меню.
    :returns: Ответ со статусом `404 Not Found` и детали.
    """
    return ORJSONResponse(
        status_code=http.HTTPStatus.NOT_FOUND,
        content={"detail": "submenu not found"},
    )


@app.exception_handler(MenuNotFoundError)
async def menu_not_found_handler(
    request: Request,
    error: MenuNotFoundError,
) -> ORJSONResponse:
    """Обрабатывает ошибку, когда меню не найдено.

    :param request: Текущий запрос.
    :param error: Перехваченная ошибка, когда меню не найдено.
    :returns: Ответ со статусом `404 Not Found` и детали.
    """
    return ORJSONResponse(
        status_code=http.HTTPStatus.NOT_FOUND,
        content={"detail": "menu not found"},
    )


@app.exception_handler(SubmenuNotIncludedInMenuError)
async def submenu_not_included_in_menu_handler(
    request: Request,
    error: SubmenuNotIncludedInMenuError,
) -> ORJSONResponse:
    """Обрабатывает ошибку, когда подменю не включено в меню.

    :param request: Текущий запрос.
    :param error: Перехваченная ошибка, когда подменю не включено в меню.
    :returns: Ответ со статусом `400 Bad Request` и детали.
    """
    return ORJSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content={"detail": "submenu not included in menu"},
    )


app.include_router(router=v1.router)  # Подключаем маршрутизатор API v1.
