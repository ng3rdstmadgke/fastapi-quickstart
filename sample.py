from typing import Callable, Optional
from pydantic import BaseModel

def try_doing(func: Callable):
    try:
        print("-----------------------")
        print(func())
    except Exception as e:
        print(e)

class User(BaseModel):
    username: str
    email: Optional[str]
    age: int

try_doing(lambda: User.parse_obj({"username": "kta", "email": "kta@example.com", "age": 31}))
try_doing(lambda: User.parse_obj({"username": "kta", "age": 31}))
try_doing(lambda: User.parse_obj({"age": 31})) # usernameがないのでエラーになる
try_doing(lambda: User.parse_obj({"username": "kta", "age": "hoge"})) # ageが数値ではないのでエラーになる