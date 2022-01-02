from typing import Optional
from sqlalchemy.orm import Session

from api import auth
from api.models.user import User as UserModel
from api.schemas.user import UserCreate as UserCreateSchema



def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreateSchema):
    hashed_password = auth.get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # dbに登録された内容をdb_itemに反映
    return db_user

def delete_user(db: Session, user: UserModel):
    db.delete(user)
    db.commit()
    return user
