from pydantic import BaseModel
from typing import Optional

class Hero_Create(BaseModel):
    name: str
    weapons: list[Weapon_Create] = []

class Hero_Out(BaseModel):
    name: str
    id: str
    weapons: list[Weapon_Out]

    class Config:
        from_attributes = True

class Inventory_Out(BaseModel):
    id: str
    user_id: str
    weapons: list[Weapon_Out] = []

class Weapon_Create(BaseModel):
    name: str

class Weapon_Out(Weapon_Create):
    id: str
    inventory_id: Optional[str]

    class Config:
        from_attributes = True
