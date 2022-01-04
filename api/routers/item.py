from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException

from api import auth
from api.db import db
from api.models.user import User
from api.schemas.item import ItemSchema, ItemCreateSchema
from api.cruds import item as crud_item

router = APIRouter()

@router.post("/items/", response_model=ItemSchema)
def create_item(
    item_schema: ItemCreateSchema,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    return crud_item.create_item(db, item_schema, current_user)

@router.get("/items/", response_model=List[ItemSchema])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    return crud_item.get_items(db, current_user.id, skip, limit)

@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(
    item_id: int,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    item = crud_item.get_item(db, current_user.id, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(
    item_id: int,
    item_schema: ItemCreateSchema,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    item = crud_item.get_item(db, current_user.id, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud_item.update_item(db, item_schema, item)

@router.delete("/items/{user_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(db.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    item = crud_item.get_item(db, current_user.id, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud_item.delete_item(db, item)
    return {"item_id": item_id}