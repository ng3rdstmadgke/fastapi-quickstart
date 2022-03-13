from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.db import db
from api.routers import item, token, user, role
from api.env import get_env

if get_env().mode == "prd":
    app = FastAPI(
        redoc_url=None,
        docs_url=None,
        openapi_url=None,
    )
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080"
    ]
else:
    # NOTE: dev環境ではAPI documentを表示
    app = FastAPI(
        redoc_url=None,
        docs_url="/api/docs",
        openapi_url="/api/docs/openapi.json"
    )
    origins = ["*"]

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

@app.get("/api/healthcheck")
async def healthcheck(
    db: Session = Depends(db.get_db),
):
    stmt = text(f"SELECT 'healthy' as message")
    row = db.execute(stmt).first()
    return {"message": row.message}