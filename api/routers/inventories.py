from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

from api.database.dependencies import get_session
from api import schemas
from api.database import models

router = APIRouter()

@router.get("/inventories",response_model=list[schemas.Base_Inventory_Out])
def get_all_inventories(session: Session = Depends(get_session)):
    db_inventories = session.query(models.Inventory).all()
    if not db_inventories:
        raise HTTPException(status_code=404,detail="There is no inventory!")
    return db_inventories


@router.get("/inventories/{inventory_id}",response_model=schemas.Base_Inventory_Out)
def get_inventory(inventory_id: str,
                  session: Session = Depends(get_session)):
    
    db_inventory = session.get(models.Inventory,inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404,detail="Inventory not found")
    return db_inventory


@router.post("/inventories/{inventory_id}")
def add_weapon_to_inventory(inventory_id: str,
                     updates: schemas.Inventory_Update,
                     session: Session = Depends(get_session)):

    #checks if the inventory exist
    db_inventory = session.get(models.Inventory,inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404,detail="Inventory not found")
    
    #checks if the weapon exist
    db_weapon = session.get(models.Weapon,updates.weapon_id)
    if not db_weapon:
        raise HTTPException(status_code=404,detail="Weapon not found")
    
    #checks if the weapon stock is enough 
    if updates.quantity > db_weapon.stock:
        raise HTTPException(status_code=400,detail="Insufficient stock!")
    
    #checks if the weapon is already in the inventory
    db_link = (session.query(models.Inventory_Weapon).filter(models.Inventory_Weapon.inventory_id==inventory_id,
                                                             models.Inventory_Weapon.weapon_id==updates.weapon_id).first())
    #if weapon exist, just add quantity
    if db_link:
        db_link.quantity += updates.quantity

    #if not exist, create new link (Inventory-Weapon)
    if not db_link:
        new_link = models.Inventory_Weapon(
            inventory_id = inventory_id,
            weapon_id = updates.weapon_id,
            quantity = updates.quantity
        )
        session.add(new_link)

    db_weapon.stock -= updates.quantity

    session.commit()
    session.refresh(db_link)
    return {"message":"Inventory updated successfully!"}


@router.put("/inventories/{inventory_id}")
def remove_weapon_from_inventory(inventory_id: str,
                     updates: schemas.Inventory_Update,
                     session: Session = Depends(get_session)):

    db_inventory = session.get(models.Inventory,inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404,detail="Inventory not found")
    
    db_weapon = session.get(models.Weapon,updates.weapon_id)
    if not db_weapon:
        raise HTTPException(status_code=404,detail="Weapon not found")
    
    db_link = (session.query(models.Inventory_Weapon).filter
                                                    (models.Inventory_Weapon.inventory_id==inventory_id,
                                                    models.Inventory_Weapon.weapon_id==updates.weapon_id).first())
    if not db_link:
        raise HTTPException(status_code=404,detail="Weapon is not in the inventory!")
    
    if db_link.quantity < updates.quantity:
        raise HTTPException(status_code=400,detail="Insufficient weapon quantity!")
    
    db_link.quantity -= updates.quantity
    db_weapon.stock += updates.quantity

    if db_link.quantity == 0:
        session.delete(db_link)

    session.commit()
    session.refresh(db_link)
    return {"message":"Inventory updated successfully!"}



