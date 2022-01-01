from typing import List, Optional
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

import crud, models, schemas, auth
from routers import item, token, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(item.router)
app.include_router(token.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.get("/me/items", response_model=List[schemas.Item])
def read_items_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user.items