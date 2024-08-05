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


    def serialize(self):
        return {
            "subcategory_id": self.subcategory_id,
            "subcategory_name": self.subcategory_name,
            "subcategory_description": self.subcategory_description,
            "subcategory_count": self.subcategory_count,
            "created_date": self.created_date,
            "created_by": self.created_by,
            "edited_date": self.edited_date,
            "edited_by": self.edited_by,
            "is_deleted": self.is_deleted,
            "subcategory_category_id": self.subcategory_category_id,
        }
