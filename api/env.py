from functools import lru_cache
from pydantic import BaseSettings

class Environment(BaseSettings):
    """環境変数を定義する構造体。
    """
    db_dialect: str
    db_driver: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key : str

@lru_cache
def get_env() -> Environment:
    """環境変数を読み込んでEnvironmentオブジェクトを生成する。
    Environmentオブジェクトはlru_cacheで保持されるため、何回も読み込まない
    """
    return Environment()