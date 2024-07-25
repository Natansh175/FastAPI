from sqlalchemy import Boolean, Column, Integer, String

from backend.db.db import Base, engine


class CategoryVO(Base):
    __tablename__ = "category_table"

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), index=True)
    category_description = Column(String(255))
    category_count = Column(Integer)
    is_deleted = Column(Boolean, default=0)
    created_date = Column(String(255))
    edited_date = Column(String(255))
