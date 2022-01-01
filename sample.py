from typing import Optional, Type
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str]
    age: int

def get_instance(model: Type["BaseModel"], data: dict):
    try:
        print("-----------------------")
        ins = model.parse_obj(data)
        print(ins)
        return ins
    except Exception as e:
        print(e)

get_instance(User, {"username": "kta", "email": "kta@example.com", "age": 31})
get_instance(User, {"username": "kta", "age": 31})
get_instance(User, {"age": 31}) # usernameがないのでエラーになる
get_instance(User, {"username": "kta", "age": "hoge"}) # ageが数値ではないのでエラーになる
get_instance(User, {"username": "kta", "age": 33, "dummy": True}) # ageが数値ではないのでエラーになる