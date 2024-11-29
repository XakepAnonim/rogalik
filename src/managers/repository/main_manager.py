"""
Модуль основного класса репозитория.
"""

from config.settings import settings
from logic.utils.common_utils import Singleton
from managers.repository.async_redis_manager import AsyncRedisManager
from managers.repository.local_redis_manager import AsyncLocalRedisManager

if settings.local_db:
    BaseClass = AsyncLocalRedisManager
else:
    BaseClass = AsyncRedisManager


class MainRepositoryManager(Singleton, BaseClass):
    """
    Основной класс репозитория, который используется для взаимодействия с данными.
    Вызывать методы необходимо с помощью "await call_or_await".
    """
