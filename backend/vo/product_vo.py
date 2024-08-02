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


    @staticmethod
    def serialize(product_vo):
        product_dict = {
            "product_id": product_vo.product_id,
            "product_name": product_vo.product_name,
            "product_description": product_vo.product_description,
            "product_price": product_vo.product_price,
            "product_quantity": product_vo.product_quantity,
            "product_image_name": product_vo.product_image_name,
            "product_image_path": product_vo.product_image_path,
            "product_category_id": product_vo.product_category_id,
            "product_subcategory_id": product_vo.product_subcategory_id,
        }
        return product_dict
