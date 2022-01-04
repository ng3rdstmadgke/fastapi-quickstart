from api import auth
from api.db.db import SessionLocal
from api.db.base import User


print("username: ", end="")
username = input().strip()
print("password: ", end="")
password = input().strip()
print("password: ", end="")
confirmation = input().strip()

if password != confirmation:
    raise Exception("パスワードが一致しません")


with SessionLocal() as session:
    hashed_password = auth.get_password_hash(password)
    db_user = User(
        username=username,
        hashed_password=hashed_password,
        is_superuser=True
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    