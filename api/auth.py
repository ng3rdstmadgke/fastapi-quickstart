import os
from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError

from api.env import get_env
from api import db
from api.models.user import User as UserModel
from api.schemas.token import (
    TokenData as TokenDataSchema
)

SECRET_KEY = get_env().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuthPasswordBearerインスタンスであると同時に、oauth2_scheme(some, parameters)のように呼び出し可能なので
# Depends(oauth2_scheme)と書くことができる
# tokenUrlにはトークンを取得するURLを指定する。(swagger UIのAuthorizeの宛先になる)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def verify_password(plain_password, hashed_password):
    # plain_passwordをそのまま引き渡して問題ない
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(db.get_db), token: str = Depends(oauth2_scheme)):
    """JWTの署名検証を行い、subに格納されているemailからUserオブジェクトを取得する
    引数のtokenには "/api/v1/token" でリターンした access_token が格納されている
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload["sub"]
        if email is None:
            raise credentials_exception
        token_data = TokenDataSchema(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
