from fastapi import FastAPI

from rogalik.server.routers import router
from rogalik.server.socket_manager import app as socketio_app


def create_server(debug: bool = True) -> FastAPI:
    """
    Create a FastAPI app with the given router.
    """
    app = FastAPI(debug=debug)

    app.include_router(router)
    app.mount("/", socketio_app)

    return app
