from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from backend.db.db import Base, engine
from backend.vo.categoryVO import CategoryVO


class SubCategoryVO(Base):
    __tablename__ = "subcategory_table"

    subcategory_id = Column(Integer, primary_key=True)
    subcategory_name = Column(String(255), index=True)
    subcategory_description = Column(String(255))
    subcategory_count = Column(Integer)
    is_deleted = Column(Boolean, default=0)
    created_date = Column(String(255))
    edited_date = Column(String(255))
    subcategory_category_id = Column(Integer, ForeignKey(CategoryVO.category_id, onupdate="CASCADE"), nullable=False)
