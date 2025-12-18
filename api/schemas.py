from pydantic import BaseModel
from typing import Optional

#==================================
            #HERO
#==================================
class Hero_Create(BaseModel):
    name: str

class Hero_Update(BaseModel):
    name: str

class Hero_Out(BaseModel):
    id: str
    name: str
    inventory: Inventory_Out

    class Config:
        from_attributes = True

#==================================
            #INVENTORY
#==================================
class Inventory_Update(BaseModel):
    weapon_id: str
    quantity: Optional[int] = 1

class Base_Inventory_Out(BaseModel):
    id: str
    hero_id: str
    inventory_weapons: list[Inventory_Weapon_Out] = []

    class Config:
        from_attributes = True

class Inventory_Out(BaseModel):
    id: str
    inventory_weapons: list[Inventory_Weapon_Out] = []

    class Config:
        from_attributes = True

#==================================
    #INVENTORY AND WEAPON LINK
#==================================
class Inventory_Weapon_Out(BaseModel):
    weapon: Weapon_Out
    quantity: int

    class Config:
        from_attributes = True

class Weapon_Inventory_Out(BaseModel):
    weapon: Weapon_Out
    quantity: int

    class Config:
        from_attributes = True


#==================================
            #WEAPON
#==================================
class Weapon_Create(BaseModel):
    name: str
    stock: int

class Weapon_Update(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None

class Base_Weapon_Out(BaseModel):
    id: str
    name: str
    stock: int

    class Config:
        from_attributes = True

class Weapon_Out(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

