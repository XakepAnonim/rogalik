"""
Модели для http запросов.
"""

from pydantic import BaseModel


class PlayerCreateModel(BaseModel):
    """
    Модель создания игрока.
    """

    username: str
    email: str
    password: str


class PlayerLoginModel(BaseModel):
    """
    Модель входа в игру.
    """

    email: str
    password: str
