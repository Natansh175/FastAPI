from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.category_vo import CategoryVO


class SubCategoryVO(Base):
    __tablename__ = "subcategory_table"

    subcategory_id = Column(Integer, primary_key=True)
    subcategory_name = Column(String(100), index=True)
    subcategory_description = Column(String(255))
    subcategory_count = Column(Integer)
    created_date = Column(String(50))
    created_by = Column(String(100), nullable=False)
    edited_date = Column(String(50))
    edited_by = Column(String(100), nullable=True)
    is_deleted = Column(Boolean, default=0)
    subcategory_category_id = Column(Integer, ForeignKey(CategoryVO.category_id, onupdate="CASCADE"), nullable=False)


    @staticmethod
    def serializer(subcategory_vo):
        subcategory_dict = {
            "subcategory_id": subcategory_vo.subcategory_id,
            "subcategory_name": subcategory_vo.subcategory_name,
            "subcategory_description": subcategory_vo.subcategory_description,
            "subcategory_count": subcategory_vo.subcategory_count,
            "subcategory_category_id": subcategory_vo.subcategory_category_id,
        }
        return subcategory_dict
