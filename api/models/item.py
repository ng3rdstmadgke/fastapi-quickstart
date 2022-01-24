from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from api.db.base_class import Base

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(MEDIUMTEXT)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="items")