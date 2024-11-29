"""
Модуль моделей для сокетов.
"""

from enum import StrEnum


class SocketRole(StrEnum):
    """
    Модель ролей для веб-сокетов.
    """

    PLAYER = "player"
    OBSERVER = "observer"
