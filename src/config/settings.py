"""
Модуль settings.py, содержит классы, функции и переменные для настроек приложения.
"""

import secrets
from pathlib import Path

from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """
    Класс, содержащий настройки приложения.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

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
    fernet_key: str = Field(
        description="Ключ шифрования fernet",
        default="",
    )
    algorithm: str = Field(
        description="Алгоритм шифрования JWT",
        default="RS256",
    )
    expiration_time: int = Field(
        description="Время действия JWT",
        default=60 * 24 * 8,  # 8 дней
    )
    verify_exp: bool = Field(
        default=True,
        description="Проверять ли время жизни токена",
    )

    # Database settings
    db_host: str = Field(
        description="Хост, на котором запущена база данных",
        default="127.0.0.1",
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
    sqlalchemy_url: str | None = None

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

    @model_validator(mode="after")
    def set_sqlalchemy_url(self) -> "Settings":
        """
        Преобразование sqlalchemy_url в формат, подходящий для sqlalchemy.
        """
        self.sqlalchemy_url = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        return self


settings = Settings()
