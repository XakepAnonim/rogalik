"""
Модели эффектов, бафов и дебафов.
"""

from pydantic import Field

from models.base import BaseModel


class DebuffsBaseModel(BaseModel):
    """
    Модель дебафа.
    """

    name: str = Field(
        description="Название дебафа",
        default="Debuff Name",
    )
    description: str = Field(
        description="Описание дебафа",
        default="Debuff Description",
    )


class BuffsBaseModel(BaseModel):
    """
    Модель бафа.
    """

    name: str = Field(
        description="Название бафа",
        default="Buff Name",
    )
    description: str = Field(
        description="Описание бафа",
        default="Buff Description",
    )


class EffectBaseModel(BaseModel):
    """
    Модель эффекта.
    """

    name: str = Field(
        description="Название эффекта",
        default="Effect Name",
    )
    description: str = Field(
        description="Описание эффекта",
        default="Effect Description",
    )
    buffs: list[BuffsBaseModel] = Field(
        description="Бафы расы",
        default=[],
    )
    debuffs: list[DebuffsBaseModel] = Field(
        description="Дебафы расы",
        default=[],
    )
