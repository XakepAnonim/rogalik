"""
Модуль http.py, содержит определение маршрутов и обработчиков для создания игры.
"""

import redis
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config.log_tools import logger
from config.settings import settings
from logic.utils.auth_utils import create_token
from logic.utils.auth_utils import jwt_authenticated
from models.client.player.base import PlayerCreateModel
from models.client.player.base import PlayerLoginModel
from models.db.base import Player
from models.db.dependencies import get_db
from models.exceptions import AuthenticationError
from models.exceptions import HTTPError
from models.repository.player.base import PlayerConfigurationModel
from models.repository.player.base import PlayerRepositoryModel

main_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@main_router.post("/login")
async def login(user: PlayerLoginModel, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Роутер для входа в игру.
    """
    get_user = await db.execute(select(Player).where(Player.email == user.email))
    existing_user = get_user.scalar()
    if not existing_user or not pwd_context.verify(user.password, existing_user.password):
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    try:
        token = create_token({"sub": existing_user.username})
    except Exception as e:
        logger.info(f"Failed to login user: {e}")
        raise AuthenticationError(str(e)) from e

    return {"access_token": token, "type": "bearer"}


@main_router.post("/register")
async def register(user: PlayerCreateModel, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Роутер для регистрации.
    """
    existing_user_by_email = await db.execute(select(Player).where(Player.email == user.email))
    if existing_user_by_email.scalar() is not None:
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    existing_user_by_username = await db.execute(select(Player).where(Player.username == user.username))
    if existing_user_by_username.scalar() is not None:
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    try:
        hashed_password = pwd_context.hash(user.password)

        new_user = Player()
        new_user.username = user.username
        new_user.email = user.email
        new_user.password = hashed_password

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        token = create_token({"sub": new_user.username})
    except Exception as e:
        logger.info(f"Failed to register user: {e}")
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return {"access_token": token, "type": "bearer"}


@main_router.post("/logout")
@jwt_authenticated
def logout(request: Request, token: str = Depends(oauth2_scheme)) -> dict:
    """
    Роутер для выхода.
    """
    try:
        redis_client = redis.StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=settings.redis_db,
        )
        redis_client.setex(f"blacklist_{token}", settings.token_expiration_time, "blacklisted")
        return {}
    except Exception as e:
        raise HTTPError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logout failed") from e


@main_router.get("/me", response_model=PlayerRepositoryModel)
@jwt_authenticated
async def get_me(request: Request, db: AsyncSession = Depends(get_db)) -> PlayerRepositoryModel:
    """
    Маршрут для получения информации о текущем пользователе.
    """
    try:
        jwt_decoded = request.state.jwt_decoded
        username = jwt_decoded["sub"]

        get_user = await db.execute(select(Player).where(Player.username == username))
        player = get_user.scalars().first()
        if not player:
            raise HTTPError(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

        return PlayerRepositoryModel(
            player_configuration=PlayerConfigurationModel(
                username=player.username,
                email=player.email,
            )
        )

    except Exception as e:
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user data") from e


@main_router.post("/story", response_model=None)
async def story() -> None:
    """
    Роутер для сюжетки игры.
    """


@main_router.post("/multiplayer", response_model=None)
async def multiplayer() -> None:
    """
    Роутер для игры в мультиплеере.
    """
