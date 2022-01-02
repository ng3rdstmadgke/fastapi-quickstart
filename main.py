from fastapi import FastAPI

from api.routers import item, token, user

app = FastAPI()
app.include_router(user.router)
app.include_router(item.router)
app.include_router(token.router)