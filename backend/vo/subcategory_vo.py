from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.category_vo import CategoryVO


class SubCategoryVO(Base):
    __tablename__ = "subcategory_table"

    subcategory_id = Column(Integer, primary_key=True)
    subcategory_name = Column(String(255), index=True)
    subcategory_description = Column(String(255))
    subcategory_count = Column(Integer)
    created_date = Column(String(255))
    created_by = Column(String(50), nullable=False)
    edited_date = Column(String(255))
    edited_by = Column(String(50), nullable=True)
    is_deleted = Column(Boolean, default=0)
    subcategory_category_id = Column(Integer, ForeignKey(CategoryVO.category_id, onupdate="CASCADE"), nullable=False)
