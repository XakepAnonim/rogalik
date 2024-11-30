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
from sqlalchemy.orm import Session

from config.settings import settings
from logic.utils.auth_utils import create_token
from logic.utils.auth_utils import jwt_authenticated
from models.client.player.base import PlayerCreateModel
from models.client.player.base import PlayerLoginModel
from models.db.base import Player
from models.db.dependencies import get_db
from models.exceptions import HTTPError

main_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@main_router.post("/login")
async def login(user: PlayerLoginModel, db: Session = Depends(get_db)) -> dict:
    """
    Роутер для входа в игру.
    """
    existing_user = db.query(Player).filter_by(username=user.username).first()
    if not existing_user:
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    if not pwd_context.verify(user.password, existing_user.password):
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    token = create_token({"sub": existing_user.username})

    return {"access_token": token, "type": "bearer"}


@main_router.post("/register")
async def register(user: PlayerCreateModel, db: Session = Depends(get_db)) -> dict:
    """
    Роутер для регистрации.
    """
    existing_user = db.query(Player).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    try:
        hashed_password = pwd_context.hash(user.password)

        new_user = Player()
        new_user.username = user.username
        new_user.email = user.email
        new_user.password = hashed_password

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_token({"sub": new_user.username})
    except Exception as e:
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


@main_router.get("/me")
@jwt_authenticated
async def get_me(request: Request, db: Session = Depends(get_db)) -> dict:
    """
    Маршрут для получения информации о текущем пользователе.
    """
    try:
        jwt_decoded = request.state.jwt_decoded
        username = jwt_decoded["sub"]

        player = db.query(Player).filter_by(username=username).first()
        if not player:
            raise HTTPError(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

        return {
            "username": player.username,
            "email": player.email,
            "characters": [char.name for char in player.characters],
        }
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
