from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from api import auth
from api import db
from api.models.user import User as UserModel
from api.schemas.item import (
    Item as ItemSchema,
    ItemCreate as ItemCreateSchema
)
from api.cruds import item as crud_item

router = APIRouter()

@router.get("/users/me/items", response_model=List[ItemSchema])
def read_items_me(current_user: UserModel = Depends(auth.get_current_active_user)):
    return current_user.items

@router.post("/users/{user_id}/items/", response_model=ItemSchema)
def create_item_for_user(user_id: int, item: ItemCreateSchema, db: Session = Depends(db.get_db)):
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)

@router.get("/items/", response_model=List[ItemSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db), token: str = Depends(auth.oauth2_scheme)):
    print(token)
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items
