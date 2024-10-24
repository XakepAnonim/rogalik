import logging
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from rogalik.settings import DB_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

character_skills = Table(
    "character_skills",
    Base.metadata,
    Column("character_id", UUID(as_uuid=True), ForeignKey("characters.id")),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id")),
)

class_roles = Table(
    "class_roles",
    Base.metadata,
    Column("class_id", UUID(as_uuid=True), ForeignKey("classes.id")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id")),
)


class EventType(PyEnum):
    SKILL_USE = "skill_use"
    ITEM_USE = "item_use"
    OTHER = "other"


class EventLog(Base):
    """
    Модель логов событий

    Attributes:
    id: UUID
    character_id: UUID идентификатор персонажа
    event_type: тип события
    details: дополнительные данные о событии (навык, изменение характеристик и т.д.)
    timestamp: время события

    """

    __tablename__ = "event_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"))
    event_type = Column(String, nullable=False)
    details = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", back_populates="logs")

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<EventLog(id={self.id}, character_id={self.character_id}, "
            f"event_type={self.event_type}, timestamp={self.timestamp})>"
        )


def log_event(character, event_type, details):
    """
    Добавляет событие в лог.
    """
    event = EventLog(character_id=character.id, event_type=event_type, details=details)
    session = SessionLocal()
    try:
        session.add(event)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при логировании события: {e}")
    finally:
        session.close()


class Player(Base):
    """
    Модель игрока у которого может быть несколько персонажей не зависимых друг от друга

    Attributes:
    id: UUID
    username: имя игрока
    characters: связь с персонажами игрока

    """

    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    characters = relationship("Character", back_populates="player")

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return f"<Player(id={self.id}, username={self.username}, created_at={self.created_at}, updated_at={self.updated_at})>"


class Skill(Base):
    """
    Модель навыков

    Attributes:
    id: UUID
    class_id: UUID идентификатор класса, к которому привязан навык
    synergy_with_class: синергия с другим классом
    name: название навыка
    description: описание навыка
    effect: эффект навыка, например, {"damage": 50, "heal": 0, "buff": "strength"}
    cooldown: перезарядка навыка в секундах
    required_level: уровень, необходимый для изучения навыка
    characters: связь с персонажами, которые имеют навык

    """

    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    synergy_with_class = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)
    effect = Column(JSON, nullable=False)
    cooldown = Column(Integer, default=0)
    required_level = Column(Integer, default=1)

    characters = relationship("Character", secondary=character_skills, back_populates="skills")

    def apply_synergy(self, target_character):
        """
        Применение синергии навыков между классами.
        Например, маг может усилить атаку воина.
        """
        log_event(target_character, "synergy_applied", {"synergy_with": str(self.synergy_with_class)})
        if self.synergy_with_class and target_character.class_id == self.synergy_with_class:
            # Пример: увеличиваем атаку цели, если она соответствует классу синергии
            target_character.base_stats["attack"] += 5

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Skill(id={self.id}, name={self.name}, description={self.description}, effect={self.effect}, "
            f"cooldown={self.cooldown}, required_level={self.required_level})>"
        )


class Item(Base):
    """
    Модель предметов

    Attributes:
    id: UUID
    name: название предмета
    description: описание предмета
    class_id: UUID идентификатор класса, к которому привязан предмет
    bonuses: бонусы предмета (например, +10 к защите)

    """

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    bonuses = Column(JSON, nullable=False)

    characters = relationship("Character", back_populates="items")

    def apply_bonuses(self, character):
        """
        Применяет бонусы предмета к персонажу.
        """
        for stat, value in self.bonuses.items():
            character.base_stats[stat] += value
        log_event(character, "item_bonus_applied", {"item_id": str(self.id), "bonuses": self.bonuses})

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Item(id={self.id}, name={self.name}, description={self.description}, "
            f"class_id={self.class_id}, bonuses={self.bonuses})>"
        )


class Character(Base):
    """
    Модель персонажа

    У каждого персонажа свой прогресс, своя история

    Attributes:
    id: UUID
    level: уровень персонажа
    experience: опыт персонажа
    player_id: UUID идентификатор игрока
    class_id: UUID идентификатор класса
    base_stats: базовые характеристики персонажа, например, {"hp": 100, "attack": 50}
    skill_points: очки навыков персонажа

    player: связь с игроком
    class_: связь с классом
    skills: связь с навыками персонажа
    events: связь с логами событий персонажа

    """

    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    base_stats = Column(JSON, nullable=False)
    skill_points = Column(Integer, default=0)

    player = relationship(Player, back_populates="characters")
    class_ = relationship("Class", back_populates="characters")
    skills = relationship(Skill, secondary=character_skills, back_populates="characters")
    events = relationship(EventLog, backref="character")
    items = relationship("Item", back_populates="characters")
    logs = relationship("EventLog", back_populates="character")

    def available_skills(self):
        """
        Возвращает список умений, которые можно изучить, основываясь на уровне персонажа.
        """
        return [skill for skill in self.skills if self.level >= skill.required_level]

    def add_experience(self, amount: int):
        """
        Добавляет опыт персонажу. Если достигнут требуемый опыт, повышает уровень.
        """
        self.experience += amount
        while self.experience >= self.experience_to_level_up():
            self.level_up()

    def experience_to_level_up(self):
        """
        Возвращает необходимое количество опыта для повышения уровня.
        """
        return self.level * 100

    def level_up(self):
        """
        Увеличивает уровень персонажа, распределяет очки навыков и улучшает характеристики.
        """
        self.level += 1
        self.experience = 0
        increment_values = {"hp": 10, "attack": 5, "defense": 3}
        for stat, increment in increment_values.items():
            self.base_stats[stat] += increment

        self.apply_class_bonuses()
        self.skill_points += 1

        print(f"{self.name} достиг уровня {self.level}!")
        print(f"Новые характеристики: {self.base_stats}")

    def apply_class_bonuses(self):
        """
        Применяет бонусы от выбранного класса персонажа, если они существуют.
        """
        if self.class_:
            self.class_.apply_bonuses(self)

    def use_skill(self, skill: Skill, target_character):
        """
        Использует навык на целевого персонажа, если навык доступен по уровню.
        """
        if self.level >= skill.required_level:
            logger.info(f"{self.name} использует {skill.name} на {target_character.name}")
            if skill.synergy_with_class:
                skill.apply_synergy(target_character)
            log_event(self, EventType.SKILL_USE.value, f"Использован {skill.name} на {target_character.name}")
            # TODO: Добавить логику, как именно навык влияет на цель
        else:
            print(f"{skill.name} недоступен для {self.name}, нужен уровень {skill.required_level}.")

    def equip_item(self, item: Item):
        """
        Экипирует предмет и применяет его бонусы.
        """
        self.items.append(item)
        item.apply_bonuses(self)

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Character(id={self.id}, level={self.level}, experience={self.experience}, "
            f"player_id={self.player_id}, class_id={self.class_id}, items={self.items})>"
        )


class Class(Base):
    """
    Модель класса

    Attributes:
    id: UUID
    name: название класса
    role: название роли, например, "маг", "танк" и т.д.
    base_stats: базовые характеристики, например, {"hp": 100, "attack": 50}
    bonuses: бонусные характеристики, например, {"critical_chance": 10, "mana_regen": 5}
    hybrid_class: флаг для гибридных классов (например, Паладин)
    characters: связь с персонажем у которого есть класс

    """

    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    base_stats = Column(JSON, nullable=False)
    bonuses = Column(JSON, nullable=True)
    hybrid_class = Column(Boolean, default=False)

    characters = relationship(Character, back_populates="class_")
    roles = relationship("Role", secondary="class_roles", back_populates="classes")

    def apply_bonuses(self, character):
        """
        Применяет бонусы класса к персонажу.
        """
        if self.bonuses:
            for stat, value in self.bonuses.items():
                character.base_stats[stat] += value
            log_event(character, "class_bonus_applied", {"class_id": str(self.id), "bonuses": self.bonuses})

    def create_character(self, player):
        """
        Создает персонажа с заданными характеристиками и умениями.
        """
        new_character = Character(
            player=player,
            class_=self,
            base_stats=self.base_stats.copy(),
        )
        self.apply_bonuses(new_character)
        return new_character

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Class(id={self.id}, name={self.name}, role={self.role}, "
            f"base_stats={self.base_stats}, bonuses={self.bonuses})>"
        )


class Role(Base):
    """
    Модель ролей персонажа

    Attributes:
    id: UUID
    name: название роли
    description: описание роли
    classes: связь с классами, которые могут выполнять данную роль

    """

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)

    classes = relationship(Class, secondary="class_roles", back_populates="roles")

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return f"<Role(id={self.id}, name={self.name})>"
