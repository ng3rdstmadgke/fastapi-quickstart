from typing import Optional
from pydantic import BaseModel


class ItemSchemaBase(BaseModel):
    """Itemの参照・作成で共通して必要になるメンバを定義したスキーマ"""
    title: str
    description: Optional[str] = None

class ItemCreateSchema(ItemSchemaBase):
    """Item作成時に利用されるスキーマ"""
    pass

class ItemSchema(ItemSchemaBase):
    """Itemの参照時や、APIからの返却データとして利用されるスキーマ"""
    id: int
    user_id: int
    
    class Config:  # innerクラス Config にはpydanticの設定を定義する
        # dictではなくORMオブジェクトを渡された場合でもデータを読み込むようにする
        # id = data["id"] で読み込めなかった場合に id = data.id でリトライする
        # 例えばuser.itemsのようにリレーションで遅延評価されるプロパティでも利用できる
        orm_mode = True  