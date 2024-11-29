"""
Модуль для эмуляции Redis в локальном окружении.
"""

import uuid
from collections.abc import Callable
from functools import cached_property
from functools import wraps
from types import TracebackType

from pydantic import BaseModel

from logic.utils.json_utils import from_json
from logic.utils.json_utils import to_json
from managers.repository.base_manager import BaseRepositoryManager
from models import exceptions


class LocalConnection:
    """
    Класс для эмуляции Redis в локальном окружении.
    """

    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        """
        Функция получения из редиса.
        """
        return self.data.get(key)

    async def set(self, key: str, value: str) -> bool:
        """
        Функция добавления в редис.
        """
        self.data[key] = value
        return True

    async def delete(self, key: str) -> bool:
        """
        Функция удаления из редиса.
        """
        try:
            del self.data[key]
        except KeyError:
            return False
        else:
            return True

    async def exists(self, key: str) -> bool:
        """
        Проверка существования.
        """
        return key in self.data

    async def flushdb(self) -> bool:
        """
        Очистка значений.
        """
        self.data = {}
        return True

    async def __aenter__(self) -> "LocalConnection":
        """
        Асинхронный вход в контекст.
        """
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """
        Асинхронный выход из контекста.
        """


class AsyncLocalRedisManager(BaseRepositoryManager):
    """
    Класс для управления виртуальным взаимодействием с базой данных.
    """

    @cached_property
    def connection(self) -> LocalConnection:
        """
        Функция подключения.
        """
        return LocalConnection()

    @staticmethod
    def _correct_connection(command_coro_func: Callable):
        """
        Внутренний декоратор для обеспечения корректного подключения к Redis перед выполнением команды.
        """

        @wraps(command_coro_func)
        async def inner(
            self: "AsyncLocalRedisManager",
            *args,
            connection: LocalConnection = None,
            **kwargs,
        ) -> Callable:
            match connection:
                case None:
                    connection = self.connection
                case LocalConnection():
                    ...
                case _:
                    msg = "Can't connect to redis"
                    raise exceptions.PythonError(msg)

            async with connection:
                return await command_coro_func(
                    self,
                    *args,
                    connection=connection,
                    **kwargs,
                )

        return inner

    @staticmethod
    def _get_uniq_name(name: str, id: uuid.UUID) -> str:
        """
        Генерирует уникальное имя, для иденцификации.
        """
        return f"{name}:{id}"

    @_correct_connection
    async def create(
        self,
        name: str,
        data: dict | BaseModel = None,
        id: uuid.UUID | None = None,
        connection: LocalConnection = None,
    ) -> uuid.UUID:
        """
        Устанавливает значение в Redis под уникальным именем.
        """
        if data is None:
            data = {}
        if id is None:
            id = uuid.uuid4()
        uniq_name = self._get_uniq_name(name, id)
        match data:
            case BaseModel():
                json_value = data.model_dump_json()
            case dict():
                json_value = to_json(data)
            case _:
                raise exceptions.PythonError
        await connection.set(uniq_name, json_value)
        return id

    @_correct_connection
    async def get_by_id(
        self,
        name: str,
        id: uuid.UUID,
        connection: LocalConnection = None,
    ) -> dict:
        """
        Извлекает значение из Redis по id.
        """
        uniq_name = self._get_uniq_name(name, id)
        json_data = await connection.get(uniq_name)
        if json_data is None:
            msg = "Invalid name or id"
            raise exceptions.PythonError(msg)
        return from_json(json_data)

    @_correct_connection
    async def delete(
        self,
        name: str,
        id: uuid.UUID,
        connection: LocalConnection = None,
    ) -> bool:
        """
        Удаляет ключ из Redis.
        """
        uniq_name = self._get_uniq_name(name, id)
        return await connection.delete(uniq_name)

    @_correct_connection
    async def update(
        self,
        name: str,
        id: uuid.UUID,
        connection: LocalConnection = None,
        **to_update_items,
    ) -> bool:
        """
        Обновляет значения из объекта Redis по id.
        """
        updatable = await self.get_by_id(name, id, connection=connection)
        for field, value in to_update_items.items():
            updatable[field] = value
        redis_key = self._get_uniq_name(name, id)
        json_data = to_json(updatable)
        return await connection.set(redis_key, json_data)

    @_correct_connection
    async def full_update(
        self,
        name: str,
        id: uuid.UUID,
        new_value: dict,
        connection: LocalConnection = None,
    ) -> bool:
        """
        Обновляет объект из Redis по id.
        """
        new_json_value = to_json(new_value)
        redis_key = self._get_uniq_name(name, id)
        return await connection.set(redis_key, new_json_value)

    @_correct_connection
    async def exists(
        self,
        name: str,
        id: uuid.UUID,
        connection: LocalConnection = None,
    ) -> bool:
        """
        Проверяет, существует ли ключ в Redis.
        """
        key = self._get_uniq_name(name, id)
        return await connection.exists(key)

    @_correct_connection
    async def clear_db(
        self,
        connection: LocalConnection = None,
    ) -> bool:
        """
        Очищает базу данных.
        """
        return await connection.flushdb()
