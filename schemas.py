from pydantic import BaseModel
from typing import Optional

class Hero_Create(BaseModel):
    name: str
    weapons: Optional[list[Weapon_Create]] = None

class Hero_Out(BaseModel):
    name: str
    id: str
    weapon: Optional[list[Weapon_Out]]

    class Config:
        from_attributes = True

class Weapon_Create(BaseModel):
    name: str

class Weapon_Out(Weapon_Create):
    id: str
    user_id: Optional[str]

    class Config:
        from_attributes = True
