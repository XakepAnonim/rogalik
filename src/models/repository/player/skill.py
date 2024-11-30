"""
Модели скиллов.
"""

import uuid

from pydantic import Field

from models.base import BaseModel
from models.constants.skill import SkillType
from models.mixins import TimestampMixin
from models.repository.extra_effects import EffectBaseModel


class SkillConfigurationModel(BaseModel):
    """
    Конфигурационная модель скилла.
    """

    type: SkillType = Field(
        description="Тип скилла",
        default=SkillType.active,
    )
    name: str = Field(
        description="Название скилла",
        default="Skill Name",
    )
    description: str = Field(
        description="Описание скилла",
        default="Skill Description",
    )
    level: int = Field(
        description="Уровень скилла",
        default=1,
    )
    required_level: int = Field(
        description="Требуемый уровень",
        default=1,
    )
    cooldown: int = Field(
        description="Время перезарядки скилла",
        default=0,
    )


class SkillBaseModel:
    """
    Базовая модель скилла.
    """

    effects: list[EffectBaseModel] = Field(
        description="Эффект скилла",
        default=EffectBaseModel(),
    )


class SkillRepositoryModel(SkillBaseModel, TimestampMixin):
    """
    Репозиторий скиллов.
    """

    skill_configuration: SkillConfigurationModel

    def id(self) -> uuid.UUID:
        """
        Возвращает id скилла.
        """
        return self.skill_configuration.uid
