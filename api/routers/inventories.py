from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

from api.database.dependencies import get_session
from api import schemas
from api.database import models

router = APIRouter()

@router.get("/inventories",response_model=list[schemas.Inventory_Out])
def get_all_inventories(session: Session = Depends(get_session)):
    db_inventories = session.query(models.Inventory).all()
    if not db_inventories:
        raise HTTPException(status_code=404,detail="There is no inventory!")
    return db_inventories

@router.get("/inventories/{inventory_id}",response_model=schemas.Inventory_Out)
def get_inventory(inventory_id: str,
                  session: Session = Depends(get_session)):
    
    db_inventory = session.get(models.Inventory,inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404,detail="Inventory not found")
    return db_inventory

@router.put("/inventories/{inventory_id}")
def update_inventory(inventory_id: str,
                     updates: schemas.Inventory_Update,
                     session: Session = Depends(get_session)):

    db_inventory = session.get(models.Inventory,inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404,detail="Inventory not found")
    
    if updates.weapon_id and updates.weapon_name:
            raise HTTPException(status_code=400,detail="Invalid input!")

    if updates.action == "add":
        if not updates.weapon_name and not updates.weapon_id:
            raise HTTPException(status_code=400,detail="Invalid action!")
        
        if updates.weapon_id:
            db_weapon = session.get(models.Weapon,updates.weapon_id)
            if not db_weapon:
                raise HTTPException(status_code=404,detail="Weapon not found")
            
            db_inventory.inventory_weapons.append(models.Inventory_Weapon(weapon = db_weapon))
            
        if updates.weapon_name:
            db_weapon = session.query(models.Weapon).filter(models.Weapon.name==updates.weapon_name).first()
            if not db_weapon:
                db_inventory.inventory_weapons.append(models.Inventory_Weapon(weapon = models.Weapon(name = updates.weapon_name)))

            if db_weapon:
                db_inventory.inventory_weapons.append(models.Inventory_Weapon(weapon = db_weapon))

    elif updates.action == "remove":
        if not updates.weapon_id:
            raise HTTPException(status_code=400,detail="Invalid action!")
        
        db_inventory_weapon = (session.query(models.Inventory_Weapon)
                            .filter(models.Inventory_Weapon.weapon_id==updates.weapon_id, 
                                    models.Inventory_Weapon.inventory_id==inventory_id)
                                    .first())
        if not db_inventory_weapon:
            raise HTTPException(status_code=404,detail="Weapon not found")
        
        session.delete(db_inventory_weapon)

    elif updates.action == "remove_all":
        db_inventory.inventory_weapons = []

    else:
       raise HTTPException(status_code=400,detail="Invalid input!")  
    
    session.commit()
    session.refresh(db_inventory)
    return {"message":"Inventory updated successfully!"}


