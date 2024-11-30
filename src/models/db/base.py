"""
Модели для базы данных.
"""

import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.models.db.mixins import TimestampMixin

engine = create_engine(settings.sqlalchemy_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@as_declarative()
class Base:
    """
    Базовая модель для всех моделей.
    """

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Идентификатор",
    )

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: PLW3201
        """
        Название таблицы.
        """
        return cls.__name__.lower()


class Player(Base, TimestampMixin):
    """
    Модель игрока.
    """

    username = Column(
        String(20),
        nullable=False,
        default="NoName",
        doc="Имя игрока",
    )
    email = Column(
        String(20),
        nullable=False,
        default="NoEmail",
        doc="Email игрока",
    )
    password = Column(
        String(20),
        nullable=False,
        default="NoPass",
        doc="Пароль игрока",
    )

    characters = relationship(
        "Character",
        back_populates="player",
        cascade="all",
        doc="Персонажи игрока",
    )


class Character(Base, TimestampMixin):
    """
    Модель персонажа.
    """

    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("player.id"),
        nullable=False,
        doc="Идентификатор игрока",
    )
    game_name = Column(
        String(20),
        nullable=False,
        default="NoName",
        doc="Имя персонажа",
    )
    experience = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Опыт",
    )
    level = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Уровень",
    )
    health = Column(
        Integer,
        nullable=False,
        default=100,
        doc="Здоровье",
    )
    speed = Column(
        Integer,
        nullable=False,
        default=10,
        doc="Скорость",
    )
    stamina = Column(
        Integer,
        nullable=False,
        default=100,
        doc="Выносливость",
    )
    damage = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Урон",
    )
    armor = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Защита",
    )
    skill_points = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Очки скилов",
    )

    player = relationship(
        "Player",
        back_populates="characters",
        doc="Игрок",
    )
    class_ = relationship(
        "Class",
        backref="characters",
        doc="Класс",
    )
    race = relationship(
        "Race",
        backref="characters",
        doc="Раса",
    )
    skills = relationship(
        "Skill",
        backref="characters",
        doc="Скиллы",
    )


class Class(Base, TimestampMixin):
    """
    Модель класса.
    """

    name = Column(
        String(20),
        nullable=False,
        default="Class Name",
        doc="Имя класса",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Class Description",
        doc="Описание класса",
    )

    effects = relationship(
        "Effect",
        backref="class",
        doc="Эффекты класса",
    )
    buffs = relationship(
        "Buff",
        backref="class",
        doc="Бафы эффекта",
    )
    debuffs = relationship(
        "Debuff",
        backref="class",
        doc="Дебафы эффекта",
    )


class Race(Base, TimestampMixin):
    """
    Модель раса.
    """

    race_type = Column(
        String(6),
        nullable=False,
        default="human",
        doc="Тип расы",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Race Description",
        doc="Описание расы",
    )

    effects = relationship(
        "Effect",
        backref="race",
        doc="Эффекты расы",
    )
    buffs = relationship(
        "Buff",
        backref="race",
        doc="Бафы эффекта",
    )
    debuffs = relationship(
        "Debuff",
        backref="race",
        doc="Дебафы эффекта",
    )


class Skill(Base, TimestampMixin):
    """
    Модель скила.
    """

    type = Column(
        String(8),
        nullable=False,
        default="active",
        doc="Тип скилла",
    )
    name = Column(
        String(20),
        nullable=False,
        default="Skill Name",
        doc="Имя скилла",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Skill Description",
        doc="Описание скилла",
    )
    level = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Уровень скилла",
    )
    required_level = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Требуемый уровень скилла",
    )
    cooldown = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Время перезарядки скилла",
    )

    effects = relationship(
        "Effect",
        backref="skill",
        doc="Эффекты скилла",
    )


class Buff(Base, TimestampMixin):
    """
    Модель бафа.
    """

    name = Column(
        String(20),
        nullable=False,
        default="Buff Name",
        doc="Название бафа",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Buff Description",
        doc="Описание бафа",
    )


class Debuff(Base, TimestampMixin):
    """
    Модель дебафа.
    """

    name = Column(
        String(20),
        nullable=False,
        default="Debuff Name",
        doc="Название дебафа",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Debuff Description",
        doc="Описание дебафа",
    )


class Effect(Base, TimestampMixin):
    """
    Модель эффекта.
    """

    name = Column(
        String(20),
        nullable=False,
        default="Effect Name",
        doc="Название эффекта",
    )
    description = Column(
        String(200),
        nullable=False,
        default="Effect Description",
        doc="Описание эффекта",
    )

    buffs = relationship(
        "Buff",
        backref="effect",
        doc="Бафы эффекта",
    )
    debuffs = relationship(
        "Debuff",
        backref="effect",
        doc="Дебафы эффекта",
    )
