from api.db import engine, Base
from api.models import user, role, item

Base.metadata.drop_all(bind=engine)