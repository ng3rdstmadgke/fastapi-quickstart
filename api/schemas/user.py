from typing import List
from pydantic import BaseModel

from api.schemas.item import Item

class UserBase(BaseModel):
    """Userの参照・作成で共通して必要になるメンバを定義したスキーマ"""
    email: str

class UserCreate(UserBase):
    """User作成時に利用されるスキーマ"""
    password: str

class User(UserBase):
    """Userの参照時や、APIからの返却データとして利用されるスキーマ"""
    id: int
    is_active: bool
    items: List[Item] = []
    
    class Config:
        orm_mode = True