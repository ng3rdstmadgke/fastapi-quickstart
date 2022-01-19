from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import item, token, user, role

app = FastAPI(
    redoc_url=None, # 本番環境では表示させない
    docs_url="/api/docs", # 本番環境では表示させない
    openapi_url="/api/docs/openapi.json" # 本番環境では表示させない
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080"
]

# CORS: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(item.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"Hello": "world"}