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
    
    new_hero = models.Hero(name = hero_input.name)
    new_hero.inventory = models.Inventory(hero = new_hero)

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
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    
    db_hero.name = hero_update.name

    session.commit()
    session.refresh(db_hero)
    return {"message":"Hero updated successfully!"}

@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: str,
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!") 
    
    session.delete(db_hero)
    session.commit()
    return {"message":"Hero deleted successfully!"}

@router.delete("/heroes")
def delete_all_heroes(session: Session = Depends(get_session)):
    session.query(models.Hero).delete()
    session.commit()