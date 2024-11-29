"""
Модуль, содержащий класс для работы с Redis.
"""

import uuid
from collections.abc import Callable
from functools import cached_property
from functools import wraps

from pydantic import BaseModel
from redis.asyncio import RedisCluster
from redis.asyncio.client import Redis

from config.settings import settings
from logic.utils.json_utils import from_json
from logic.utils.json_utils import to_json
from managers.repository.base_manager import BaseRepositoryManager
from models import exceptions


class AsyncRedisManager(BaseRepositoryManager):
    """
    Класс для управления асинхронным взаимодействием с Redis.
    """

    @cached_property
    def connection(self) -> RedisCluster | Redis:
        """
        Функция подключения к редису.
        """
        return (
            Redis(
                host=settings.host,
                port=settings.port,
                password=settings.password,
                decode_responses=True,
            )
            if not settings.cluster
            else RedisCluster(
                host=settings.host,
                port=settings.port,
                password=settings.password,
                socket_timeout=5,
                decode_responses=True,
            )
        )

    @staticmethod
    def _correct_connection(command_coro_func: Callable):
        """
        Внутренний декоратор для обеспечения корректного подключения к Redis перед выполнением команды.
        """

        @wraps(command_coro_func)
        async def inner(
            self: "AsyncRedisManager",
            *args,
            connection: Redis | RedisCluster = None,
            **kwargs,
        ) -> Callable:
            match connection:
                case None:
                    connection = self.connection
                case Redis() | RedisCluster():
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
    def _get_uniq_name(name: str, uid: uuid.UUID) -> str:
        """
        Генерирует уникальное имя, для идентификации.
        """
        return f"{name}:{uid}"

    @_correct_connection
    async def create(
        self,
        name: str,
        data: dict | BaseModel = None,
        id: uuid.UUID | None = None,
        connection: Redis | RedisCluster = None,
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
        connection: Redis = None,
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
        connection: Redis | RedisCluster = None,
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
        connection: Redis | RedisCluster = None,
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
        connection: Redis | RedisCluster = None,
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
        connection: Redis | RedisCluster = None,
    ) -> bool:
        """
        Функция проверки существования.
        """
        key = self._get_uniq_name(name, id)
        return await connection.exists(key)

    @_correct_connection
    async def clear_db(self, connection: Redis | RedisCluster = None) -> bool:
        """
        Функция очистки бд
        """
        return await connection.flushdb()
