"""
Миксины.
"""

from datetime import datetime

from pydantic import Field

from models.repository.extra_effects import BuffsBaseModel
from models.repository.extra_effects import DebuffsBaseModel
from models.repository.extra_effects import EffectBaseModel


class TimestampMixin:
    """
    Миксин для даты создания и обновления
    """

    created_at: datetime = Field(
        description="Дата создания",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Дата обновления",
        default_factory=datetime.now,
    )


class ExtraEffectsMixin:
    """
    Миксин для эффектов, бафов и дебафов
    """

    effects: list[EffectBaseModel] = Field(
        description="Эффекты",
        default=[],
    )
    buffs: list[BuffsBaseModel] = Field(
        description="Бафы",
        default=[],
    )
    debuffs: list[DebuffsBaseModel] = Field(
        description="Дебафы",
        default=[],
    )
