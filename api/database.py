
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://r00t:r00t1234@mido-dev02-devrds-db-back.cxh1e43zwtop.ap-northeast-1.rds.amazonaws.com/fastapi_quickstart?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#SessionLocal = scoped_session(sessionmaker(autocommit = False, autoflush = True, bind=engine))
SessionLocal = sessionmaker(autocommit = False, autoflush = True, bind=engine)
Base = declarative_base()