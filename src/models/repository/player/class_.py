"""
Модели классов.
"""

import uuid

from pydantic import BaseModel
from pydantic import Field

from models.mixins import ExtraEffectsMixin
from models.mixins import TimestampMixin


class ClassConfigurationModel(BaseModel):
    """
    Конфигурационная модель класса.
    """

    uid: uuid.UUID = Field(
        description="Уникальный идентификатор класса",
        default_factory=uuid.uuid4,
    )
    name: str = Field(
        description="Название класса",
        default="Class name",
    )
    description: str = Field(
        description="Описание класса",
        default="Class description",
    )


class ClassRepositoryModel(BaseModel, TimestampMixin):
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
