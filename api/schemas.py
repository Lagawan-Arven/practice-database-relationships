from pydantic import BaseModel
from typing import Optional

class Hero_Create(BaseModel):
    name: str

class Hero_Out(BaseModel):
    name: str
    id: str
    inventory: Inventory_Out

    class Config:
        from_attributes = True

# one-to-one

class Inventory_Update(BaseModel):
    weapon_name: Optional[str]
    weapon_id: Optional[str]
    action: str

class Inventory_Out(BaseModel):
    id: str
    user_id: str
    weapons: list[Weapon_Out] = []

    class Config:
        from_attributes = True

# one-to-many

class Weapon_Create(BaseModel):
    name: str

class Weapon_Out(Weapon_Create):
    id: str
    inventory_id: Optional[str]

    class Config:
        from_attributes = True
