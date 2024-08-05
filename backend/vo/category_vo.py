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


    def serialize(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_description": self.category_description,
            "category_count": self.category_count,
            "created_date": self.created_date,
            "created_by": self.created_by,
            "edited_date": self.edited_date,
            "edited_by": self.edited_by,
            "is_deleted": self.is_deleted,
        }
