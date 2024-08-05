from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.category_vo import CategoryVO
from backend.vo.subcategory_vo import SubCategoryVO


class ProductVO(Base):
    __tablename__ = "product_table"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), index=True)
    product_description = Column(String(255))
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    product_image_name = Column(String(150), nullable=False)
    product_image_path = Column(String(150), nullable=False)
    created_date = Column(String(50))
    created_by = Column(String(100), nullable=False)
    edited_date = Column(String(50))
    edited_by = Column(String(100), nullable=True)
    is_deleted = Column(Boolean, default=0)
    product_category_id = Column(Integer,
                                 ForeignKey(CategoryVO.category_id, onupdate="CASCADE"), nullable=False)
    product_subcategory_id = Column(Integer,
                                    ForeignKey(SubCategoryVO.subcategory_id, onupdate="CASCADE"), nullable=False)


    def serialize(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "product_price": self.product_price,
            "product_quantity": self.product_quantity,
            "product_image_name": self.product_image_name,
            "product_image_path": self.product_image_path,
            "created_date": self.created_date,
            "created_by": self.created_by,
            "edited_date": self.edited_date,
            "edited_by": self.edited_by,
            "is_deleted": self.is_deleted,
            "product_category_id": self.product_category_id,
            "product_subcategory_id": self.product_subcategory_id,
        }
