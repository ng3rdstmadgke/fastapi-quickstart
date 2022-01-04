from fastapi import FastAPI

from api.routers import item, token, user, role

app = FastAPI(
    docs_url="/api/docs",
    redoc_url=None
)
app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(item.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"Hello": "world"}