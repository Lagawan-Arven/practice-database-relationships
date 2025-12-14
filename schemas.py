from pydantic import BaseModel
from typing import Optional

class Hero_Create(BaseModel):
    name: str
    weapon: Weapon_Create

class Hero_Out(BaseModel):
    name: str
    id: str
    weapon: Weapon_Out

    class Config:
        from_attributes = True

class Weapon_Create(BaseModel):
    name: str

class Weapon_Out(Weapon_Create):
    id: str
    user_id: str

    class Config:
        from_attributes = True
