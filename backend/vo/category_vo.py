from sqlalchemy import Boolean, Column, Integer, String

from backend.db.db import Base


class CategoryVO(Base):
    __tablename__ = "category_table"

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), index=True)
    category_description = Column(String(255))
    category_count = Column(Integer)
    created_date = Column(String(100))
    created_by = Column(String(100), nullable=False)
    edited_date = Column(String(50))
    edited_by = Column(String(100), nullable=True)
    is_deleted = Column(Boolean, default=0)


    @staticmethod
    def serialize(category_vo):
        category_dict = {
            "category_id": category_vo.category_id,
            "category_name": category_vo.category_name,
            "category_description": category_vo.category_description,
            "category_count": category_vo.category_count,
        }
        return category_dict
