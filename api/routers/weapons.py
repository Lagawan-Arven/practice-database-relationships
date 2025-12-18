from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from api.database.dependencies import get_session
from api import schemas
from api.database import models

router = APIRouter()

@router.get("/weapons",response_model=list[schemas.Base_Weapon_Out])
def get_all_weapons(session: Session = Depends(get_session)):

    db_weapons = session.query(models.Weapon).all()
    if not db_weapons:
        raise HTTPException(status_code=404,detail="There is no weapon!")
    
    return db_weapons

@router.post("/weapons")
def add_weapon(weapon_input: schemas.Weapon_Create,
               session: Session = Depends(get_session)):
    
    new_weapon = models.Weapon(
        name = weapon_input.name,
        stock = weapon_input.stock
    )
    session.add(new_weapon)
    session.commit()
    session.refresh(new_weapon)
    return {"message":"Weapon added successfully!"}

@router.put("/weapons/{weapon_id}")
def update_weapon(weapon_id: str,
                  weapon_update: schemas.Weapon_Update,
                  session: Session = Depends(get_session)):
    
    db_weapon = session.query(models.Weapon).filter(models.Weapon.id==weapon_id).first()
    if not db_weapon:
        raise HTTPException(status_code=404,detail="Weapon not found!")

    if weapon_update.name and weapon_update.stock:
        db_weapon.name = weapon_update.name
        db_weapon.stock = weapon_update.stock
    elif weapon_update.name and not weapon_update.stock:
        db_weapon.name = weapon_update.name
    elif not weapon_update.name and weapon_update.stock:
        db_weapon.stock = weapon_update.stock

    session.commit()
    session.refresh(db_weapon)
    return {"message":"Weapon updated successfully!"}

@router.delete("/weapons/{weapon_id}")
def delete_weapon(weapon_id: str,
                  session: Session = Depends(get_session)):
    
    db_weapon = session.query(models.Weapon).filter(models.Weapon.id==weapon_id).first()
    if not db_weapon:
        raise HTTPException(status_code=404,detail="Weapon not found!")
    
    session.delete(db_weapon)
    session.commit()
    return {"message":"Weapon deleted successfully!"}

@router.delete("/weapons")
def delete_all_weapons(session: Session = Depends(get_session)):
    session.query(models.Weapon).delete()
    session.commit()