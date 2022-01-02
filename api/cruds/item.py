from sqlalchemy.orm import Session

from api.models.item import Item as ItemModel
from api.schemas.item import ItemCreate as ItemCreateSchema

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ItemModel).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: ItemCreateSchema, user_id: int):
    db_item = ItemModel(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # dbに登録された内容をdb_itemに反映
    return db_item