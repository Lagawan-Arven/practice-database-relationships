from sqlalchemy import Integer,String,ForeignKey,Column,DateTime
from sqlalchemy.orm import relationship,declarative_base
from datetime import datetime,timezone
from uuid import uuid4

from api.database.database import engine

Base = declarative_base()

class Hero(Base):
    __tablename__ = "Heroes"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    name = Column(String)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    inventory = relationship("Inventory",back_populates="hero",cascade="all, delete-orphan",uselist=False)
    
class Inventory(Base):
    __tablename__ = "Inventories"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    user_id = Column(String(4),ForeignKey("Heroes.id",ondelete="CASCADE"),unique=True,nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    hero = relationship("Hero",back_populates="inventory",uselist=False)
    weapons = relationship("Weapon",back_populates="inventory")

class Weapon(Base):
    __tablename__ = "Weapons"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    name = Column(String)   
    inventory_id = Column(String(4),ForeignKey("Inventories.id",ondelete="SET NULL"),unique=False,nullable=True)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    inventory = relationship("Inventory",back_populates="weapons")

Base.metadata.create_all(bind=engine)