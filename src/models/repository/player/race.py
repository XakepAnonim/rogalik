"""
Модель рас.
"""

import uuid
from typing import Any

from pydantic import Field

from models.base import BaseModel
from models.constants.race import RaceType
from models.mixins import ExtraEffectsMixin
from models.mixins import TimestampMixin
from models.repository.player.skill import SkillRepositoryModel


class RaceConfigurationModel(BaseModel):
    """
    Конфигурационная модель рассы.
    """

    race: RaceType = Field(
        description="Тип расы персонажа",
        default=RaceType.human,
    )
    description: str = Field(
        description="Описание расы",
        default="Description race",
    )


class RaceBaseModel:
    """
    Базовая модель расы.
    """

    skills: list[SkillRepositoryModel] = Field(
        description="Скиллы расы",
        default=[],
    )


class RaceRepositoryModel(RaceBaseModel, TimestampMixin):
    """
    Репозиторий расы.
    """

    effects: ExtraEffectsMixin
    race_configuration: RaceConfigurationModel

    @property
    def id(self) -> uuid.UUID:
        """
        Возвращает id расы.
        """
        return self.race_configuration.uid

    def get_effects(self) -> list[Any]:
        """
        Возвращает список эффектов расы.
        """
        return self.effects.effects

    def get_buffs(self) -> list[Any]:
        """
        Возвращает список бафов расы.
        """
        return self.effects.buffs

    def get_debuffs(self) -> list[Any]:
        """
        Возвращает список дебафов расы.
        """
        return self.effects.debuffs
