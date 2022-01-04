from typing import List
from pydantic import BaseModel

from api.schemas.item import ItemSchema
from api.schemas.role import RoleSchema

class UserSchemaBase(BaseModel):
    """Userの参照・作成で共通して必要になるメンバを定義したスキーマ"""
    username: str

class UserCreateSchema(UserSchemaBase):
    """User作成時に利用されるスキーマ"""
    password: str

class UserSchema(UserSchemaBase):
    """Userの参照時や、APIからの返却データとして利用されるスキーマ"""
    id: int
    is_superuser: bool
    is_active: bool
    items: List[ItemSchema] = []
    roles: List[RoleSchema] = []
    
    class Config:
        orm_mode = True