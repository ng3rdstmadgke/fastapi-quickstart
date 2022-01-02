from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException

from api import auth
from api import db
from api.models.user import User as UserModel
from api.schemas.user import (
    User as UserSchema,
    UserCreate as UserCreateSchema
)
from api.cruds import user as crud_user

router = APIRouter()

# Depends(Callable[..., Any]) は引数に取った関数を実行してその実行結果を返す。
#  Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(db.get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    return crud_user.create_user(db=db, user=user)

@router.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    users = crud_user.get_users(db, skip=skip, limit = limit)
    return users

@router.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: UserModel = Depends(auth.get_current_active_user)):
    return current_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(db.get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db.get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, db_user)
    return {"user_id": user_id}
