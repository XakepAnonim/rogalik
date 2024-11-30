"""
Модуль работы с аутентификацией токена
"""

from collections.abc import Callable
from collections.abc import Coroutine
from datetime import datetime
from datetime import timedelta
from functools import wraps
from typing import Any
from typing import TypeVar

import jwt
import pydantic
import redis
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Request
from jwt import ExpiredSignatureError
from jwt import InvalidAudienceError
from jwt import InvalidTokenError
from jwt import MissingRequiredClaimError
from starlette import status

from config.settings import settings
from models import exceptions
from models.exceptions import AuthenticationError
from models.exceptions import HTTPShortError
from models.exceptions import SocketIOError

TReturnType = TypeVar("TReturnType")


class JWKeyCache:
    """
    Кэш ключей для проверки аутентификации JWT токенов, использующий Redis.
    """

    def __init__(self) -> None:
        """
        Создает кэш ключей и загружает публичный ключ.
        Если ключ отсутствует, он будет создан.
        """
        self.redis_client = redis.StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=settings.redis_db,
        )

        self._algorithm = settings.algorithm
        self._fernet_key = settings.fernet_key

        if not self.redis_client.exists("public_key") or not self.redis_client.exists("private_key"):
            self.generate_key_pair()

    def generate_key_pair(self) -> None:
        """
        Генерация новой пары ключей (приватного и публичного).
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        cipher_suite = Fernet(self._fernet_key)
        encrypted_private_key = cipher_suite.encrypt(private_key_pem)
        self.redis_client.set("private_key", encrypted_private_key)

        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.redis_client.set("public_key", public_key_pem)

    async def get_public_key(self) -> str:
        """
        Получить публичный ключ для проверки токена из Redis.
        """
        public_key = await self.redis_client.get("public_key")
        if public_key is None:
            raise ValueError("Public key not found in Redis")
        return public_key.decode("utf-8")

    async def get_private_key(self) -> rsa.RSAPrivateKey:
        """
        Получить приватный ключ из Redis.
        """
        encrypted_private_key = await self.redis_client.get("private_key")
        if encrypted_private_key is None:
            raise ValueError("Private key not found in Redis")

        cipher_suite = Fernet(self._fernet_key)
        private_key_pem = cipher_suite.decrypt(encrypted_private_key)

        return serialization.load_pem_private_key(
            private_key_pem,
            password=None,
        )


def jwt_authenticated(
    func: Callable[..., Coroutine[Any, Any, TReturnType]],
) -> Callable[..., Coroutine[Any, Any, TReturnType]]:
    """
    Декоратор для проверки и декодирования JWT.
    Используется для проверки токенов до выполнения функции.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> TReturnType:
        """
        Проверяет наличие и валидность JWT в headers, декодирует его и передает обернутой функции.
        """
        request: Request | None = kwargs.get("request")
        error_cls: type[SocketIOError | HTTPShortError]

        if request is not None:
            token = request.headers.get("Authorization", "")
            error_cls = HTTPShortError
        else:
            token = f"Bearer {kwargs.get('jwt', '')}"
            error_cls = SocketIOError

        kwargs["jwt_decoded"] = validate_token(token, error_cls)

        return await func(*args, **kwargs)

    return wrapper


def create_token(payload: dict) -> str:
    """
    Функция для создания JWT токена.
    """
    expiration_time = settings.expiration_time
    expiration_date = datetime.utcnow() + timedelta(seconds=expiration_time)

    payload["exp"] = expiration_date

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def validate_token(token: str, error_cls: type[Exception] = AuthenticationError) -> dict:
    """
    Функция для валидации JWT токена.
    Проверяет наличие токена, его префикс и валидность подписи.

    :param token: Токен с префиксом Bearer
    :param error_cls: Класс ошибки для выброса
    """
    prefix = "Bearer "

    if not token.startswith(prefix):
        msg = "Invalid token header. No credentials provided."
        raise error_cls(msg)

    token = token.removeprefix(prefix)
    jwks = JWKeyCache()

    try:
        pub_key = jwks.get_public_key()

        jwt_decoded = jwt.decode(
            token,
            pub_key,
            algorithms=[settings.algorithm],
            options={
                "verify_aud": False,
                "verify_iat": False,
                "verify_exp": settings.verify_exp,
            },
        )
    except MissingRequiredClaimError as e:
        raise error_cls(str(e)) from e
    except ExpiredSignatureError as e:
        msg = "Signature expired"
        raise error_cls(msg) from e
    except InvalidAudienceError as e:
        msg = "JWT audience mismatch"
        raise error_cls(msg) from e
    except InvalidTokenError as e:
        msg = "JWT decode error"
        raise error_cls(msg) from e
    except pydantic.ValidationError as e:
        msg = f"Token content is invalid: {e}"
        raise error_cls(msg) from e

    return jwt_decoded


def http_authenticated(
    func: Callable[..., Coroutine[Any, Any, TReturnType]],
) -> Callable[..., Coroutine[Any, Any, TReturnType]]:
    """
    Декоратор для проверки токена HTTP-запроса.
    Используется для HTTP роутов для проверки аутентификации.
    """

    @wraps(func)
    async def inner(request: Request, *args: Any, **kwargs: Any) -> TReturnType:
        """
        Проверяет существование ключа авторизации в заголовке и валидирует его.
        """
        api_key: str | None = request.headers.get("Authorization")

        if api_key is None:
            raise exceptions.HTTPError(detail="Authorization key does not exist", status_code=status.HTTP_403_FORBIDDEN)

        return await func(request, *args, **kwargs)

    return inner
