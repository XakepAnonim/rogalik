"""
Модуль, содержащий базовые модели данных для SocketIO сообщений, определяет базовые схемы модели,
которые могут использоваться для валидации и сериализации входящих и исходящих сообщений через SocketIO.
"""

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from pydantic import field_validator

json_ = str


class BaseActionModel(BaseModel):
    """
    Базовая модель данных для WebSocket.
    """

    action: str
    data: dict | list | None = None


class ActionRequestModel(BaseActionModel):
    """
    Базовая модель данных для валидации входящих запросов WebSocket.
    """

    action: str
    data: dict | list = Field(default_factory=dict)

    @field_validator("action")
    def action_must_endswith_client(cls, v: str) -> str:
        """
        Валидатор для проверки окончания action на _client.
        """
        if not v.endswith("_client"):
            raise ValidationError("action must be endswith _client")
        return v.removesuffix("_client")


class ActionResponseModel(BaseActionModel):
    """
    Базовая модель данных для валидации исходящих ответов WebSocket.
    """

    action: str
    data: dict | list | None = None

    @field_validator("action")
    def action_must_endswith_server(cls, v: str) -> str:
        """
        Валидатор для проверки окончания action на _server.
        """
        if not v.endswith("_server"):
            v += "_server"
        return v


class BaseRequestActionDataModel(BaseModel):
    """
    Базовая модель для данных входящих запросов Websocket.
    """

    class Config:
        """
        Конфиг для базовой модель для данных входящих запросов Websocket
        """

        extra = "forbid"


class BaseResponseActionDataModel(BaseModel):
    """
    Базовая модель для данных исходящих запросов Websocket.
    """

    delta: int | None = None


class NoResponseModel(BaseResponseActionDataModel):
    """
    Модель для действий, которые не возвращают ответ.
    """
