from fastapi import FastAPI

from api.routers import item, token, user, role

app = FastAPI(
    redoc_url=None, # 本番環境では表示させない
    docs_url="/api/docs", # 本番環境では表示させない
    openapi_url="/api/docs/openapi.json" # 本番環境では表示させない
)
app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(item.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"Hello": "world"}