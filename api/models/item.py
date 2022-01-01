from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), index=True)
    description = Column(String(191))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="items")