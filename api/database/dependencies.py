from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from api.database.database import mysession
from api.auth import SECRET_KEY,ALGORITHM

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_session():
    session = mysession()
    try:
        yield session
    finally:
        session.close()

def get_current_user(token: str = Depends(oauth2scheme),session: Session = Depends(get_session)):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get("id"))
    except:
        raise HTTPException(status_code=406,detail="Invalid token!")
    
    '''db_user = session.query(schemas.User).filter(schemas.User.id==customer_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="Customer not found!")
    
    return db_user'''