from api import db
from api import auth
from api.models import *


print("username: ", end="")
username = input().strip()
print("password: ", end="")
password = input().strip()
print("password: ", end="")
confirmation = input().strip()

if password != confirmation:
    raise Exception("パスワードが一致しません")


with db.SessionLocal() as session:
    hashed_password = auth.get_password_hash(password)
    db_user = user.User(
        username=username,
        hashed_password=hashed_password,
        is_superuser=True
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    