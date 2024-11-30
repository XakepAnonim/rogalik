"""
Модели игрока и персонажа.
"""

import uuid

from pydantic import Field

from models.base import BaseModel
from models.mixins import TimestampMixin
from models.repository.player.class_ import ClassRepositoryModel
from models.repository.player.race import RaceRepositoryModel
from models.repository.player.skill import SkillRepositoryModel


class PlayerConfigurationModel(BaseModel):
    """
    Конфигурационная модель игрока.
    """

    username: str = Field(
        description="Ник пользователя в игре",
        default="NoName",
    )
    email: str = Field(
        description="Email пользователя в игре",
        default="NoEmail",
    )
    password: str = Field(
        description="Пароль пользователя в игре",
        default="NoPassword",
    )


class PlayerRepositoryModel(TimestampMixin):
    """
    Репозиторий игрока.
    """

    player_configuration: PlayerConfigurationModel

    @property
    def id(self) -> uuid.UUID:
        """
        Возвращает id игрока.
        """
        return self.player_configuration.uid


class CharacterConfigurationModel(BaseModel):
    """
    Конфигурационная модель персонажа.
    """

    game_name: str = Field(
        description="Ник пользователя в игре",
        default="NoName",
    )
    experience: float = Field(
        description="Опыт персонажа",
        default=0,
    )
    level: int = Field(
        description="Уровень персонажа",
        default=1,
    )
    health: int = Field(
        description="Здоровье персонажа",
        default=100,
    )
    speed: int = Field(
        description="Скорость персонажа",
        default=10,
    )
    stamina: int = Field(
        description="Выносливость персонажа",
        default=100,
    )
    damage: int = Field(
        description="Урон персонажа",
        default=1,
    )
    armor: int = Field(
        description="Броня персонажа",
        default=0,
    )
    skill_points: int = Field(
        description="Очки навыков",
        default=0,
    )


class CharacterBaseModel:
    """
    Базовая модель персонажа.
    """

    class_: ClassRepositoryModel = Field(
        description="Класс персонажа",
    )
    race: RaceRepositoryModel = Field(
        description="Раса персонажа",
    )
    skills: list[SkillRepositoryModel] = Field(
        description="Скиллы персонажа",
    )


class CharacterRepositoryModel(TimestampMixin):
    """
    Репозиторий персонажа.
    """

    player: PlayerRepositoryModel
    character_configuration: CharacterConfigurationModel

    @property
    def id(self) -> uuid.UUID:
        """
        Возвращает id персонажа.
        """
        return self.character_configuration.uid

    @property
    def player_id(self) -> uuid.UUID:
        """
        Возвращает id игрока.
        """
        return self.player.id
