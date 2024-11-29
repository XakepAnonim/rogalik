"""
Модуль, содержащий инструменты для связывания SocketIO сообщений с обработчиками.
"""

from collections.abc import Callable


class ActionRoutes(dict):
    """
    Класс для управления SocketIO маршрутами. Является словарем,
    где ключом является 'action' из JSON, а значением — функция, обрабатывающая это действие.
    """

    def register_action(self, action_name: str) -> Callable:
        """
        Декоратор для регистрации действия по его названию.
        """

        def decorator(func: Callable):
            self[action_name] = func
            return func

        return decorator


action_routes = ActionRoutes()
