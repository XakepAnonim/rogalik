"""
Dependencies.
"""

from models.db.base import SessionLocal


async def get_db() -> None:
    """
    Получение базы данных.
    """
    async with SessionLocal() as session:
        yield session
