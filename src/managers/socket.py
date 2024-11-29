"""
Модуль socket.py, содержит базовый класс менеджера SocketIO.
"""

from typing import Union

import socketio

from config.log_tools import logger
from managers.actions.action_routes import action_routes
from managers.repository.main_manager import MainRepositoryManager
from models.constants.socket import SocketRole

sio = socketio.AsyncServer(async_mode="asgi")


class SocketNamespaceStore:
    """
    Хранилище SocketIO-соединений.

    Хранит соединения SocketIO и наблюдателей.
    """

    def __init__(self) -> None:
        self.connections: dict[str, SocketMainNamespace] = {}
        self.observers: dict[str, set[SocketMainNamespace]] = {}

    def get_connection(self, sid: str) -> Union["SocketMainNamespace", None]:
        """
        Функция получения подключения.
        """
        return self.connections.get(sid)

    def get_observers(self, sid: str) -> set["SocketMainNamespace"]:
        """
        Функция получения наблюдателей.
        """
        return self.observers.get(sid, set())

    def add_connection(self, sid: str, namespace: "SocketMainNamespace") -> None:
        """
        Функция создания SocketIO подключения.
        """
        match namespace.role:
            case SocketRole.PLAYER:
                self.connections[sid] = namespace
            case SocketRole.OBSERVER:
                self.observers.setdefault(
                    sid,
                    set(),
                ).add(namespace)

    def remove_connection(self, sid: str, namespace: "SocketMainNamespace") -> None:
        """
        Функция удаления SocketIO подключения.
        """
        match namespace.role:
            case SocketRole.PLAYER:
                del self.connections[sid]
            case SocketRole.OBSERVER:
                self.observers[sid].remove(namespace)

    def clear(self, sid: str) -> None:
        """
        Функция очистки SocketIO подключения.
        """
        del self.connections[sid]
        del self.observers[sid]


class SocketMainNamespace(socketio.AsyncNamespace):
    """
    Основной класс нэймспэйса SocketIO.
    Этот класс определяет основную функциональность для нэймспэйса SocketIO.
    Он предоставляет методы для подключения, отправки и получения сообщений
    через SocketIO, а также для обработки входящих сообщений и управления
    жизненным циклом соединения.
    """

    routes = action_routes
    store = SocketNamespaceStore()

    def __init__(self, namespace: str | None = None) -> None:
        super().__init__(namespace)
        self.role: SocketRole | None = None
        self.redis_repository = MainRepositoryManager()

    async def on_connect(self, sid: str, environ: dict) -> None:
        """
        Этот метод вызывается при подключении SocketIO соединения.
        """
        logger.info(f"Client {sid} connected")

    async def on_disconnect(self, sid: str) -> None:
        """
        Обработка отключения клиента через on_disconnect.
        """
        logger.info(f"Client {sid} disconnected")

    async def on_action(self, sid: str, data: dict) -> None:
        """
        Обработка действий клиента через action_routes и сохранение данных в Redis.
        """
        action_name = data.get("action")
        if action_name in action_routes:
            response = await action_routes[action_name](sid, data)
            # # Пример использования Redis для сохранения данных
            # await self.redis_repository.set_value(f"client:{sid}:action", action_name)
            await self.emit("response", response, to=sid)
        else:
            await self.emit("error", {"message": f"Unknown action: {action_name}"}, to=sid)


sio.register_namespace(SocketMainNamespace("/socket"))
