"""
Модуль app.py, содержит экземпляр класса FastAPI приложения.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.routers.http import main_router
from config.routers.socket import connect_router
from config.routers.socket import socket_app
from config.settings import settings


def server_init() -> FastAPI:
    """
    Инициализация приложения.
    """
    app = FastAPI(
        title="Rogalik",
        description="Рогалик",
        version="1.0",
        debug=settings.debug,
        openapi_url=f"{settings.api_key}/openapi.json" if settings.enable_swagger else "",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(main_router)
    app.include_router(connect_router)
    app.mount("/", socket_app)

    return app


app = server_init()
