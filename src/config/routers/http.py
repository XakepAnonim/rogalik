"""
Модуль http.py, содержит определение маршрутов и обработчиков для создания игры.
"""

from fastapi import APIRouter

main_router = APIRouter()


@main_router.post("/login", response_model=None)
async def login() -> None:
    """
    Роутер для входа в игру.
    """


@main_router.post("/register", response_model=None)
async def register() -> None:
    """
    Роутер для регистрации.
    """


@main_router.post("/logout", response_model=None)
async def logout() -> None:
    """
    Роутер для выхода из игры.
    """


@main_router.post("/story", response_model=None)
async def story() -> None:
    """
    Роутер для сюжетки игры.
    """


@main_router.post("/multiplayer", response_model=None)
async def multiplayer() -> None:
    """
    Роутер для игры в мультиплеере.
    """
