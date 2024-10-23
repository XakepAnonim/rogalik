from sqlalchemy import Column, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rogalik.settings import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Player(Base):
    """
    Player table
    """

    __tablename__ = "player"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)

    def __repr__(self):
        """
        Represent player as a string
        """
        return f"<Player(id={self.id}, username={self.username})>"
