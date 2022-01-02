from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://r00t:r00t1234@mido-dev02-devrds-db-back.cxh1e43zwtop.ap-northeast-1.rds.amazonaws.com/fastapi_quickstart?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = True, bind=engine)
Base = declarative_base()

def get_db():
    print("create session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("close session")