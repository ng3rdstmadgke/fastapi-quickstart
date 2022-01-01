from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

router = APIRouter()

@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    print(token)
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
