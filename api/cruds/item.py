from typing import Optional, List
from sqlalchemy.orm import Session

from api.models.item import Item
from api.models.user import User
from api.schemas.item import ItemCreateSchema

# Session API: https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# Query API: https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query

def get_item(db: Session, user_id: int, item_id: int) -> Optional[Item]:
    return db \
        .query(Item) \
        .filter(Item.user_id == user_id, Item.id == item_id) \
        .first()

def get_items(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    return db \
        .query(Item) \
        .filter(Item.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

def create_item(db: Session, item_schema: ItemCreateSchema, user: User) -> Item:
    item = Item(**item_schema.dict())
    user.items.append(item)
    db.add(user)
    db.commit()
    db.refresh(item)
    return item

def update_item(db: Session, item_schema: ItemCreateSchema, item: Item) -> Item:
    item.title = item_schema.title
    item.description = item_schema.description
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item: Item):
    db.delete(item)
    db.commit()
