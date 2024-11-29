"""
Модуль settings.py, содержит классы, функции и переменные для настроек приложения.
"""

import secrets
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """
    Класс, содержащий настройки приложения.
    """

    # Server settings
    host: str = Field(
        description="Хост, на котором запущен сервер",
        default="127.0.0.1",
    )
    port: int = Field(
        description="Порт, на котором запущен сервер",
        default=8080,
    )
    debug: bool = Field(
        description="Включает отладочную информацию",
        default=False,
    )
    api_key: str = Field(description="Ключ для работы с API", default="/api/v1")
    enable_swagger: bool = Field(
        description="Включение/отключение swagger документации",
        default=False,
    )
    cors_allowed_origins: str = Field(
        description="Разрешенные cors",
        default="http://localhost:8000",
    )

    # JWT settings
    secret_key: str = Field(
        description="Секретный ключ для шифрования JWT",
        default=secrets.token_urlsafe(32),
    )
    algorithm: str = Field(
        description="Алгоритм шифрования JWT",
        default="HS256",
    )
    expiration_time: int = Field(
        description="Время действия JWT",
        default=60 * 24 * 8,
    )

    # Database settings
    db_host: str = Field(
        description="Хост, на котором запущена база данных",
        default="127.0.0.1",
    )
    db_port: int = Field(
        description="Порт, на котором запущена база данных",
        default=5432,
    )
    db_name: str = Field(
        description="Название базы данных",
        default="postgres",
    )
    db_user: str = Field(
        description="Имя пользователя базы данных",
        default="postgres",
    )
    db_password: str = Field(
        description="Пароль пользователя базы данных",
        default="postgres",
    )
    sqlalchemy_url: str = Field(
        description="Строка с параметрами подключения к базе данных",
        default=f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    )

    # Redis settings
    redis_host: str = Field(
        description="Хост, на котором запущен редис",
        default="127.0.0.1",
    )
    redis_port: int = Field(
        description="Порт, на котором запущен редис",
        default=6379,
    )
    redis_password: str = Field(
        description="Пароль редиса",
        default="",
    )
    redis_db: int = Field(
        description="Номер базы данных редиса",
        default=0,
    )
    local_db: bool = Field(
        description="Использовать ли локальную базу данных",
        default=True,
    )
    cluster: bool = Field(
        description="Используется ли редис кластер",
        default=False,
    )


settings = Settings()
