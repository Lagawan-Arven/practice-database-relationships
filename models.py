from sqlalchemy import Integer,String,ForeignKey,Column
from sqlalchemy.orm import relationship,declarative_base
from uuid import uuid4

from database import engine

Base = declarative_base()

class Hero(Base):
    __tablename__ = "Heroes"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    name = Column(String)

    weapon = relationship("Weapon",back_populates="hero",uselist=False)

class Weapon(Base):
    __tablename__ = "Weapons"

    id = Column(String(4),primary_key=True,default=lambda: uuid4().hex[:4],unique=True,nullable=False)
    name = Column(String)   
    user_id = Column(String(4),ForeignKey("Heroes.id",ondelete="SET NULL"),unique=True,nullable=True)

    hero = relationship("Hero",back_populates="weapon")

Base.metadata.create_all(bind=engine)