from fastapi import APIRouter

from cafeteria.external.v1.routes import dishes, menus, submenus

__all__ = ["router"]

router = APIRouter(prefix="/api/v1")

router.include_router(
    router=dishes.router,
    tags=["dishes"],
)
router.include_router(
    router=menus.router,
    tags=["menus"],
)
router.include_router(
    router=submenus.router,
    tags=["submenus"],
)
