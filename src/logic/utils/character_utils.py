"""
Модуль содержит утилиты для работы с игроком.
"""

import asyncio
import uuid

from logic.utils.common_utils import call_or_await
from managers.repository.main_manager import MainRepositoryManager
from models.constants.character import CHARACTER_MODEL_NAME
from models.repository.player.base import CharacterRepositoryModel


async def get_character(
    character_repo_id: str,
    repository_connection: MainRepositoryManager = None,
) -> CharacterRepositoryModel:
    """
    Получение модели персонажа.
    """
    repository = MainRepositoryManager()
    character_dict = await call_or_await(
        repository.get_by_id,
        CHARACTER_MODEL_NAME,
        character_repo_id,
        connection=repository_connection,
    )

    return CharacterRepositoryModel.model_validate(character_dict)
    # match character_dict["game"]["mode"]:
    #     case GameMode.solo.value | GameMode.tutorial.value:
    #         return CharacterRepositoryModel.model_validate(character_dict)
    #     case GameMode.realtime.value:
    #         return PlayerRepositoryRealTimeModel.model_validate(character_dict)
    #     case _:
    #         raise ValueError("not found game_mode")


async def get_characters(
    character_repo_ids: list[str],
    repository_connection: MainRepositoryManager = None,
) -> list[CharacterRepositoryModel]:
    """
    Получение моделей персонажев.
    """
    return [await get_character(character_id, repository_connection) for character_id in character_repo_ids]


async def update_character(
    character: CharacterRepositoryModel,
    repository_connection: MainRepositoryManager = None,
    **to_update_params,
) -> None:
    """
    Обновление информации о персонаже.
    """
    character_repo_id = get_character_repository_id(character)
    repository = MainRepositoryManager()

    for key, value in to_update_params.items():
        setattr(character, key, value)
    await call_or_await(
        repository.full_update,
        CHARACTER_MODEL_NAME,
        character_repo_id,
        character,
        connection=repository_connection,
    )


async def update_characters(
    characters: list[CharacterRepositoryModel],
    repository_connection: MainRepositoryManager = None,
) -> None:
    """
    Обновление информации о персонажах.
    """
    await asyncio.gather(*[update_character(character, repository_connection) for character in characters])


def get_character_repository_id(
    character: CharacterRepositoryModel = None,
    game_id: uuid.UUID | None = None,
    character_id: uuid.UUID | None = None,
) -> str:
    """
    Объединяет id персонажа и игры, для хранения в репозитории.
    """

    def new_id(gid: uuid.UUID, pid: uuid.UUID) -> str:
        return f"{gid}:{pid}"

    if character:
        return new_id(character.game.id, character.character_configuration.uid)

    return new_id(game_id, character_id)


def get_character_id_from_repository(character_repository_id: str) -> uuid:
    """
    Вычленяет id персонажа из его id в репозитории.
    """
    return uuid.UUID(character_repository_id.split(":")[1])


async def add_character_to_repository(
    character: CharacterRepositoryModel,
    repository_connection: MainRepositoryManager = None,
) -> None:
    """
    Добавление персонажа в репозиторий.
    """
    repository = MainRepositoryManager()
    await call_or_await(
        repository.create,
        CHARACTER_MODEL_NAME,
        character.model_dump(),
        get_character_repository_id(character=character),
        connection=repository_connection,
    )
