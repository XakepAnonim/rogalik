"""
Модуль сервиса логики SocketIO.
"""

from config.log_tools import logger
from managers.actions.action_routes import action_routes


@action_routes.register_action("my_event")
async def handle_my_event(sid: str, data: dict) -> dict:
    """
    Обработка события.
    """
    logger.info(f"Обрабатываем событие от {sid} с данными: {data}")
    return {"message": "Данные успешно обработаны"}
