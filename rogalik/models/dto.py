import uuid

from pydantic import BaseModel
from pydantic.v1 import validator


class Skill(BaseModel):
    """
    Схема для навыка.

    Attributes:
    name: str
    description: str
    effect: Dict[str, int]  # Здесь словарь, который будет представлять эффекты
    cooldown: int
    required_level: int

    """

    name: str
    description: str | None
    effect: dict[str, int]
    cooldown: int
    required_level: int

    @validator("required_level")
    def check_required_level(cls, v):
        """
        Проверка на недопустимое значение.
        """
        if v < 1:
            raise ValueError("required_level должен быть больше 0")
        return v


class Item(BaseModel):
    """
    Схема для предметов.

    Attributes:
    name: str
    description: str
    bonuses: Dict[str, int]  # Бонусы предмета

    """

    name: str
    description: str
    bonuses: dict[str, int]


class BaseStats(BaseModel):
    """
    Схема для базовых характеристик класса и персонажа.
    """

    hp: int
    attack: int
    defense: int


class Character(BaseModel):
    """
    Схема для персонажей.

    Attributes:
    level: int
    experience: int
    player_id: UUID
    class_id: UUID
    skills: list[Skill]
    base_stats: BaseStats

    """

    level: int
    experience: int
    player_id: uuid.UUID
    class_id: uuid.UUID
    skills: list[Skill]
    base_stats: BaseStats
    items: list[Item] | None = None

    @validator("level", "experience")
    def check_positive(cls, v):
        """
        Проверка на недопустимое значение.
        """
        if v < 0:
            raise ValueError("level и experience должны быть неотрицательными")
        return v


class Class(BaseModel):
    """
    Схема для классов.

    Attributes:
    name: str
    role: str
    base_stats: BaseStats  # Базовая статистика класса {"hp": 100, "attack": 50}
    bonuses: Optional[Dict[str, int]] = None  # Бонусные характеристики класса

    """

    name: str
    role: str
    base_stats: BaseStats
    bonuses: dict[str, int] | None = None


class Role(BaseModel):
    """
    Схема для ролей.

    Attributes:
    name: str
    description: str

    """

    name: str
    description: str | None
