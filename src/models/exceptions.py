"""
Модуль, содержащий пользовательские классы исключений, определяет пользовательские классы исключений,
которые могут быть использованы для обработки различных ошибок и исключительных ситуаций в приложении.
"""

from fastapi import HTTPException
from fastapi import status
from starlette.exceptions import WebSocketException


class PythonError(Exception):
    """
    Класс пользовательского исключения для ошибок Python.
    """

    def __init__(self, message: str = "Ошибка") -> None:
        self.message = message


class SocketIOError(WebSocketException):
    """
    Класс пользовательского исключения для ошибок SocketIO.
    """

    def __init__(
        self,
        reason: str | None = None,
        code: int = status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
    ):
        self.code = code
        self.reason = reason or ""


class HTTPError(HTTPException):
    """
    Класс пользовательского исключения для ошибок в HTTP запросе.
    """


class HTTPShortError(HTTPError):
    """
    Класс HTTP ошибки с кодом 403.
    """

    def __init__(self, text: str) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=text)


class AuthenticationError(PythonError):
    """
    Класс пользовательского исключения для ошибок аутентификации.
    """
