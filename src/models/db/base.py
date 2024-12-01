"""
Модели для базы данных.
"""

import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from models.db.mixins import TimestampMixin

engine = create_async_engine(settings.sqlalchemy_url, echo=True)
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


character_skill = Table(
    "character_skill",
    Base.metadata,
    Column("character_id", UUID(as_uuid=True), ForeignKey("character.id")),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skill.id")),
)


class_buff = Table(
    "class_buff",
    Base.metadata,
    Column("class_id", UUID(as_uuid=True), ForeignKey("class.id")),
    Column("buff_id", UUID(as_uuid=True), ForeignKey("buff.id")),
)

class_debuff = Table(
    "class_debuff",
    Base.metadata,
    Column("class_id", UUID(as_uuid=True), ForeignKey("class.id")),
    Column("debuff_id", UUID(as_uuid=True), ForeignKey("debuff.id")),
)

race_buff = Table(
    "race_buff",
    Base.metadata,
    Column("race_id", UUID(as_uuid=True), ForeignKey("race.id")),
    Column("buff_id", UUID(as_uuid=True), ForeignKey("buff.id")),
)

race_debuff = Table(
    "race_debuff",
    Base.metadata,
    Column("race_id", UUID(as_uuid=True), ForeignKey("race.id")),
    Column("debuff_id", UUID(as_uuid=True), ForeignKey("debuff.id")),
)


class Player(Base, TimestampMixin):
    """
    Модель игрока.
    """

    username = Column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
        doc="Имя игрока",
    )
    email = Column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
        doc="Email игрока",
    )
    password = Column(
        String(60),
        nullable=False,
        doc="Пароль игрока",
    )

    characters = relationship(
        "Character",
        back_populates="player",
        doc="Список персонажей",
    )


class Character(Base, TimestampMixin):
    """
    Модель персонажа.
    """

    game_name = Column(
        String(32),
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

    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("player.id"),
        doc="Идентификатор игрока",
    )
    player = relationship(
        "Player",
        back_populates="characters",
        doc="Игрок",
    )

    class_id = Column(
        UUID(as_uuid=True),
        ForeignKey("class.id"),
        doc="Идентификатор класса",
    )
    race_id = Column(
        UUID(as_uuid=True),
        ForeignKey("race.id"),
        doc="Идентификатор расы",
    )

    character_class = relationship(
        "Class",
        doc="Класс персонажа",
    )
    race = relationship(
        "Race",
        doc="Раса персонажа",
    )
    skills = relationship(
        "Skill",
        secondary=character_skill,
        back_populates="characters",
        doc="Скиллы персонажа",
    )


class Class(Base, TimestampMixin):
    """
    Модель класса.
    """

    name = Column(
        String(32),
        nullable=False,
        default="Class Name",
        doc="Имя класса",
    )
    description = Column(
        String(256),
        nullable=False,
        default="Class Description",
        doc="Описание класса",
    )

    effects = relationship(
        "Effect",
        back_populates="character_class",
        doc="Эффекты класса",
    )
    buffs = relationship(
        "Buff",
        secondary=class_buff,
        back_populates="classes",
        doc="Бафы класса",
    )
    debuffs = relationship(
        "Debuff",
        secondary=class_debuff,
        back_populates="classes",
        doc="Дебафы класса",
    )


class Race(Base, TimestampMixin):
    """
    Модель раса.
    """

    type = Column(
        String(6),
        nullable=False,
        default="human",
        doc="Тип расы",
    )
    description = Column(
        String(256),
        nullable=False,
        default="Race Description",
        doc="Описание расы",
    )

    characters = relationship(
        "Character",
        back_populates="race",
        doc="Список персонажей",
    )
    effects = relationship(
        "Effect",
        back_populates="race",
        doc="Эффекты расы",
    )
    buffs = relationship(
        "Buff",
        secondary=race_buff,
        back_populates="races",
        doc="Бафы расы",
    )
    debuffs = relationship(
        "Debuff",
        secondary=race_debuff,
        back_populates="races",
        doc="Дебафы расы",
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
        String(32),
        nullable=False,
        default="Skill Name",
        doc="Имя скилла",
    )
    description = Column(
        String(256),
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
        back_populates="skill",
        doc="Эффекты скилла",
    )
    characters = relationship(
        "Character",
        secondary=character_skill,
        back_populates="skills",
        doc="Список персонажей",
    )


class Buff(Base, TimestampMixin):
    """
    Модель бафа.
    """

    name = Column(
        String(32),
        nullable=False,
        default="Buff Name",
        doc="Название бафа",
    )
    description = Column(
        String(256),
        nullable=False,
        default="Buff Description",
        doc="Описание бафа",
    )

    classes = relationship(
        "Class",
        secondary=class_buff,
        back_populates="buffs",
        doc="Классы бафа",
    )
    races = relationship(
        "Race",
        secondary=race_buff,
        back_populates="buffs",
        doc="Расы бафа",
    )


class Debuff(Base, TimestampMixin):
    """
    Модель дебафа.
    """

    name = Column(
        String(32),
        nullable=False,
        default="Debuff Name",
        doc="Название дебафа",
    )
    description = Column(
        String(256),
        nullable=False,
        default="Debuff Description",
        doc="Описание дебафа",
    )

    classes = relationship(
        "Class",
        secondary=class_debuff,
        back_populates="debuffs",
        doc="Классы дебафа",
    )
    races = relationship(
        "Race",
        secondary=race_debuff,
        back_populates="debuffs",
        doc="Классы дебафа",
    )


class Effect(Base, TimestampMixin):
    """
    Модель эффекта.
    """

    name = Column(
        String(32),
        nullable=False,
        default="Effect Name",
        doc="Название эффекта",
    )
    description = Column(
        String(256),
        nullable=False,
        default="Effect Description",
        doc="Описание эффекта",
    )

    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skill.id"),
        doc="Идентификатор скилла",
    )
    character_class_id = Column(
        UUID(as_uuid=True),
        ForeignKey("class.id"),
        doc="Идентификатор класса",
    )
    race_id = Column(
        UUID(as_uuid=True),
        ForeignKey("race.id"),
        doc="Идентификатор расы",
    )

    skill = relationship(
        "Skill",
        back_populates="effects",
        doc="Скиллы использующие эффект",
    )
    character_class = relationship(
        "Class",
        back_populates="effects",
        doc="Классы персонажа использующие эффект",
    )
    race = relationship(
        "Race",
        back_populates="effects",
        doc="Расы персонажа использующие эффект",
    )
