from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

from api.database.dependencies import get_session
from api import schemas
from api.database import models

router = APIRouter()

@router.get("/inventories",response_model=schemas.Inventory_Out)
def get_all_inventories(session: Session = Depends(get_session)):
    db_inventories = session.query(models.Inventory).all()
    if not db_inventories:
        raise HTTPException(status_code=404,detail="There is not inventory!")
    return db_inventories

@router.put("/inventories/{inventory_id}")
def update_inventory(inventory_id: str):
    pass

