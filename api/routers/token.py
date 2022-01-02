from typing import Optional
from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api import auth
from api import db
from api.cruds import token as crud_token

router = APIRouter()

@router.post("/token")
def login_for_access_token(db: Session = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm は username, password, scope, grant_type といったメンバを持つ
    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
    user = crud_token.authenticate_user(db, form_data.username, form_data.password)
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
