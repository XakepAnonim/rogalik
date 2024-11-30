"""
Модуль моделей для сокетов.
"""

from enum import StrEnum


class SocketRole(StrEnum):
    """
    Модель ролей для сокетов.
    """

    PLAYER = "player"
    OBSERVER = "observer"
