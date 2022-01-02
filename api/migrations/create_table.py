from db import engine, Base

from models import user, item

Base.metadata.create_all(bind=engine)
