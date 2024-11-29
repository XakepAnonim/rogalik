"""
Модуль, содержащий определение маршрутов и обработчиков для SocketIO подключения.
"""

import socketio
from fastapi import APIRouter

from managers.socket import sio

connect_router = APIRouter()

socket_app = socketio.ASGIApp(sio)
