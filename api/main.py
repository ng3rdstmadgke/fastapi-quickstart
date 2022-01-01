from typing import List

from fastapi import Depends, FastAPI
from db import SessionLocal, engine

import crud, models, schemas, auth
from routers import item, token, user

app = FastAPI()
app.include_router(user.router)
app.include_router(item.router)
app.include_router(token.router)


@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.get("/me/items", response_model=List[schemas.Item])
def read_items_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user.items