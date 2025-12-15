from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import Optional

from api import schemas
from api.database.dependencies import get_session
from api.database import models

router = APIRouter()

@router.post("/heroes")
def add_hero(hero_input: schemas.Hero_Create,
             session: Session = Depends(get_session)):
    
    new_hero = models.Hero(
        name = hero_input.name
    )

    if hero_input.weapons:
        new_hero.weapons = list[models.Weapon(name = hero_input.weapons.name)]

    session.add(new_hero)
    session.commit()
    session.refresh(new_hero)
    return {"message":"Hero added successfully!"}

@router.get("/heroes",response_model=list[schemas.Hero_Out])
def get_all_heroes(session: Session = Depends(get_session)):

    db_heroes = session.query(models.Hero).all()
    if not db_heroes:
        raise HTTPException(status_code=404,detail="There is no hero yet!")
    
    return db_heroes

@router.get("/heroes/{hero_id}",response_model=schemas.Hero_Out)
def get_hero(hero_id: str,
             session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    return db_hero

@router.put("/heroes/{hero_id}")
def update_hero(hero_id: str,
                hero_update: schemas.Hero_Create,
                weapon_id: Optional[str] = None,
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    
    db_hero.name = hero_update.name

    if weapon_id and hero_update.weapon == None:
        db_weapon = session.query(models.Weapon).filter(models.Weapon.id==weapon_id).first()
        if not db_weapon:
           raise HTTPException(status_code=404,detail="Hero not found!") 
        if db_weapon.hero:
            raise HTTPException(status_code=400,detail="Weapon already possessed by other hero!")

        if db_hero.weapon:
            db_weapon.user_id = None
            session.flush()
            db_hero.weapon = db_weapon
        else:
            db_hero.weapon = db_weapon

    elif hero_update.weapon and weapon_id == None:
        new_weapon = models.Weapon(name = hero_update.weapon.name)
        session.add(new_weapon)
        session.flush()

        if db_hero.weapon:
            db_hero.weapon = None
            session.flush()
            db_hero.weapon = new_weapon
        else:
            db_hero.weapon = new_weapon

    elif weapon_id and hero_update.weapon:
        raise HTTPException(status_code=400,detail="Invalid action!")

    session.commit()
    session.refresh(db_hero)
    return {"message":"Hero updated successfully!"}

@router.post("/heroes/{hero_id}")
def set_hero_weapon_to_null(hero_id: str,
                            session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    
    db_hero.weapon = None
    session.commit()
    session.refresh(db_hero)
    {"message":"Weapon set to null successfully!"}

@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: str,
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!") 
    
    session.delete(db_hero)
    session.commit()
    return {"message":"Hero deleted successfully!"}