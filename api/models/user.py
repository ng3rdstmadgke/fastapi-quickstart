from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(191), unique=True, index=True)
    hashed_password = Column(String(191))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="user")