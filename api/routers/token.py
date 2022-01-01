from typing import Optional
from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter()

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """emailとpasswordで認証を行う"""
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        return None
    if not auth.verify_password(password, db_user.hashed_password):
        return None
    return db_user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    # tokenには "/token" でリターンした access_token が格納されている
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload["sub"]
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm は username, password, scope, grant_type といったメンバを持つ
    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
