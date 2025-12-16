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
    inventory_weapons = relationship("Inventory_Weapon",back_populates="inventories", cascade="all, delete-orphan")

class Inventory_Weapon(Base):
    __tablename__ = "Inventory_Weapons"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    inventory_id = Column(String(4),ForeignKey("Inventories.id",ondelete="CASCADE"),unique=False)
    weapon_id = Column(String(4),ForeignKey("Weapons.id",ondelete="CASCADE"),unique=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    inventories = relationship("Inventory",back_populates="inventory_weapons")
    weapons = relationship("Weapon",back_populates="weapon_inventories")

class Weapon(Base):
    __tablename__ = "Weapons"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    name = Column(String)   
    added_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    weapon_inventories = relationship("Inventory_Weapon",back_populates="weapons", cascade="all, delete-orphan")

Base.metadata.create_all(bind=engine)