"""
Модуль common_utils.py, предоставляет различные утилитарные функции и классы для работы приложения.
"""

from inspect import isawaitable
from typing import Any


async def call_or_await(func_or_coro: Any, *args, **kwargs) -> Any:
    """
    Вызов функции или ожидание корутины. Если результат вызова функции является корутиной, ожидается его выполнение.

    :param func_or_coro: Функция или корутина для вызова.
    """
    result = func_or_coro(*args, **kwargs)
    if isawaitable(result):
        result = await result
    return result


class Singleton:
    """
    Класс Singleton для создания одного экземпляра класса.
    """

    _instance = None

    def __new__(cls: "Singleton", *args, **kwargs):
        """
        Создание экземпляра синглтона
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
