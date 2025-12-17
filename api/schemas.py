from pydantic import BaseModel
from typing import Optional

class Hero_Create(BaseModel):
    name: str

class Hero_Out(BaseModel):
    name: str
    id: str
    inventory: Hero_Inventory_Out

    class Config:
        from_attributes = True

#==========================
# one-to-one
#==========================

class Inventory_Update(BaseModel):
    weapon_name: Optional[str]
    weapon_id: Optional[str]
    action: str

class Hero_Inventory_Out(BaseModel):
    id: str
    inventory_weapons: list[Inventory_Weapon_Out] = []

    class Config:
        from_attributes = True

class Inventory_Out(BaseModel):
    id: str
    user_id: str
    inventory_weapons: list[Inventory_Weapon_Out] = []

    class Config:
        from_attributes = True

#===========================
# link for many-to-many
#===========================

class Inventory_Weapon_Out(BaseModel):
    weapon: Nested_Weapon_Out

    class Config:
        from_attributes = True

class Weapon_Inventory_Out(BaseModel):
    inventory_id: str

    class Config:
        from_attributes = True

#===========================
# link for many-to-many
#===========================

class Weapon_Create(BaseModel):
    name: str

class Weapon_Out(Weapon_Create):
    id: str
    weapon_inventories: list[Weapon_Inventory_Out] = []

    class Config:
        from_attributes = True

class Nested_Weapon_Out(Weapon_Create):
    id: str

    class Config:
        from_attributes = True
