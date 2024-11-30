"""
Модели классов.
"""

import uuid

from pydantic import Field

from models.base import BaseModel
from models.mixins import ExtraEffectsMixin
from models.mixins import TimestampMixin


class ClassConfigurationModel(BaseModel):
    """
    Конфигурационная модель класса.
    """

    name: str = Field(
        description="Название класса",
        default="Class name",
    )
    description: str = Field(
        description="Описание класса",
        default="Class description",
    )


class ClassRepositoryModel(TimestampMixin):
    """
    Репозиторий класса.
    """

    effects: ExtraEffectsMixin
    class_configuration: ClassConfigurationModel

    @property
    def id(self) -> uuid.UUID:
        """
        Возвращает id класса.
        """
        return self.class_configuration.uid
