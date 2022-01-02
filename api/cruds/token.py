from typing import Optional
from sqlalchemy.orm import Session

from api import auth
from api.models.user import User as UserModel

def authenticate_user(db: Session, email: str, password: str) -> Optional[UserModel]:
    """emailとpasswordで認証を行う"""
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user is None:
        return None
    if not auth.verify_password(password, db_user.hashed_password):
        return None
    return db_user