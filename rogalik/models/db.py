import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from rogalik.settings import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

character_abilities = Table(
    "character_abilities",
    Base.metadata,
    Column("character_id", UUID(as_uuid=True), ForeignKey("characters.id")),
    Column("ability_id", UUID(as_uuid=True), ForeignKey("abilities.id")),
)


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


class Character(Base):
    """
    Модель персонажа

    У каждого персонажа свой прогресс, своя история

    Attributes:
    id: UUID
    level: уровень персонажа
    experience: опыт персонажа
    player_id: UUID идентификатор игрока
    player: связь с игроком
    class_id: UUID идентификатор класса
    class_: связь с классом
    abilities: связь с умениями персонажа
    base_stats: базовые характеристики персонажа, например, {"hp": 100, "attack": 50}

    """

    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    base_stats = Column(JSON, nullable=False)

    player = relationship("Player", back_populates="characters")
    class_ = relationship("Class", back_populates="characters")
    abilities = relationship("Ability", secondary=character_abilities, back_populates="characters")

    def available_abilities(self):
        """
        Возвращает список умений, которые можно изучить.
        """
        return [ability for ability in self.abilities if self.level >= ability.required_level]

    def add_experience(self, amount: int):
        """
        Добавляет опыт персонажу.
        """
        self.experience += amount
        while self.experience >= self.experience_to_level_up():
            self.level_up()

    def experience_to_level_up(self):
        """
        Возвращает опыт, который нужно для уровня персонажа.
        """
        return self.level * 100

    def level_up(self):
        """
        Увеличивает уровень персонажа.
        """
        self.level += 1
        self.experience = 0
        increment_values = {"hp": 10, "attack": 5, "defense": 3}
        for stat, increment in increment_values.items():
            self.base_stats[stat] += increment

        print(f"{self.player.username}'s character leveled up to level {self.level}!")
        print(f"New base stats: {self.base_stats}")

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Character(id={self.id}, level={self.level}, experience={self.experience}, "
            f"player_id={self.player_id}, class_id={self.class_id})>"
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
    characters: связь с персонажем у которого есть класс

    """

    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    base_stats = Column(JSON, nullable=False)
    bonuses = Column(JSON, nullable=True)

    characters = relationship("Character", back_populates="class_")

    def apply_bonuses(self, character):
        """
        Применяет бонусы класса к персонажу.
        """
        if self.bonuses:
            for stat, value in self.bonuses.items():
                character.base_stats[stat] += value

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


class Ability(Base):
    """
    Модель умений

    Attributes:
    id: UUID
    name: название умения
    description: описание умения
    effect: эффект умения, например, {"damage": 50, "heal": 0, "buff": "strength"}
    cooldown: перезарядка умения в секундах
    required_level: уровень, необходимый для изучения умения

    """

    __tablename__ = "abilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    effect = Column(JSON, nullable=False)
    cooldown = Column(Integer, default=0)
    required_level = Column(Integer, default=1)

    characters = relationship("Character", secondary=character_abilities, back_populates="abilities")

    def __repr__(self):
        """
        Возвращает строковое представление объекта.
        """
        return (
            f"<Ability(id={self.id}, name={self.name}, description={self.description}, effect={self.effect}, "
            f"cooldown={self.cooldown}, required_level={self.required_level})>"
        )
