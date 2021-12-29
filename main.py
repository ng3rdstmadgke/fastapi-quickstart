from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic.schema import schema
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

# OAuthPasswordBearerインスタンスであると同時に、oauth2_scheme(some, parameters)のように呼び出し可能なので
# Depends(oauth2_scheme)と書くことができる
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Depends(Callable[..., Any]) は引数に取った関数を実行してその実行結果を返す。
#  Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit = limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print(token)
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm には
    db_user = crud.get_user_by_email(db, form_data.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = form_data.password + "notreallyhashed"
    if hashed_password != db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # tokenエンドポイントの戻り値はaccess_tokenとtoken_typeを含むdictである必要がある
    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
    return {"access_token": db_user.email, "token_type": "bearer"}



def get_current_active_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # tokenには "/token" でリターンした access_token が格納されている
    email = token
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return db_user


@app.get("/myuser", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user