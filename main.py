from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session
import schemas
import models

app = FastAPI()

@app.post("/heroes")
def add_hero(hero_input: schemas.Hero_Create,
             session: Session = Depends(get_session)):
    
    new_hero = models.Hero(
        name = hero_input.name,
        weapon = models.Weapon(name = hero_input.weapon.name)
    )
    session.add(new_hero)
    session.commit()
    session.refresh(new_hero)
    return {"message":"Hero added successfully!"}

@app.get("/heroes",response_model=list[schemas.Hero_Out])
def get_all_heroes(session: Session = Depends(get_session)):

    db_heroes = session.query(models.Hero).all()
    if not db_heroes:
        raise HTTPException(status_code=404,detail="There is no hero yet!")
    
    return db_heroes

@app.get("/heroes/{hero_id}",response_model=schemas.Hero_Out)
def get_hero(hero_id: str,
             session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    return db_hero

@app.put("/heroes/{hero_id}")
def update_hero(hero_id: str,
                hero_update: schemas.Hero_Create,
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!")
    
    db_hero.name = hero_update.name #type: ignore
    if db_hero.weapon:
        db_hero.weapon.name = hero_update.weapon.name
    else:
        new_weapon = models.Weapon(name = hero_update.weapon.name, hero = db_hero)
        session.add(new_weapon)
    
    session.commit()
    session.refresh(db_hero)
    return {"message":"Hero updated successfully!"}

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: str,
                session: Session = Depends(get_session)):
    
    db_hero = session.query(models.Hero).filter(models.Hero.id==hero_id).first()
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found!") 
    
    session.delete(db_hero)
    session.commit()
    return {"message":"Hero deleted successfully!"}