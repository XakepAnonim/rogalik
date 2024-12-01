"""
Модели эффектов, бафов и дебафов.
"""

import uuid

from pydantic import BaseModel
from pydantic import Field


class DebuffsBaseModel(BaseModel):
    """
    Модель дебафа.
    """

    uid: uuid.UUID = Field(
        description="Уникальный идентификатор дебафа",
        default_factory=uuid.uuid4,
    )
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

    uid: uuid.UUID = Field(
        description="Уникальный идентификатор бафа",
        default_factory=uuid.uuid4,
    )
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

    uid: uuid.UUID = Field(
        description="Уникальный идентификатор эффекта",
        default_factory=uuid.uuid4,
    )
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
