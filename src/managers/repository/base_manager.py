"""
Модуль, содержащий абстрактный базовый класс для управления репозиторием.
"""

import uuid
from abc import ABC
from abc import abstractmethod
from functools import cached_property
from types import TracebackType

from pydantic import BaseModel


class BaseRepositoryManager(ABC):
    """
    Базовый класс менеджера репозитория.
    """

    @abstractmethod
    @cached_property
    def connection(self) -> None:
        """
        Абстрактный атрибут для получения подключения к репозиторию.
        """

    @abstractmethod
    def create(
        self,
        name: str,
        data: dict | BaseModel,
    ) -> bool:
        """
        Абстрактный метод для установления значения в репозиторий.
        """

    @abstractmethod
    def get_by_id(
        self,
        name: str,
        id: uuid.UUID,
    ) -> dict:
        """
        Абстрактный метод для получения значения из репозитория по заданному имени и идентификатору.
        """

    @abstractmethod
    def delete(
        self,
        name: str,
        id: uuid.UUID,
    ) -> bool:
        """
        Абстрактный метод для удаления значения из репозитория по заданному имени и идентификатору.
        """

    @abstractmethod
    def update(
        self,
        name: str,
        id: uuid.UUID,
        **to_update_items,
    ) -> bool:
        """
        Абстрактный метод для обновления значения из репозитория по заданному имени и идентификатору.
        """

    @abstractmethod
    async def full_update(
        self,
        name: str,
        id: uuid.UUID,
        new_value: dict,
    ) -> bool:
        """
        Абстрактный метод для полной замены значения из репозитория по заданному имени и идентификатору.
        """

    async def __aenter__(self):
        """
        Функция асинхронного входа в контекст.
        """
        return await self.connection.__aenter__()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ):
        """
        Функция асинхронного выхода из контекста.
        """
        return await self.connection.__aexit__(exc_type, exc_val, exc_tb)
