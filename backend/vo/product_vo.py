from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from backend.db.db import Base
from backend.vo.category_vo import CategoryVO
from backend.vo.subcategory_vo import SubCategoryVO


class ProductVO(Base):
    __tablename__ = "product_table"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), index=True)
    product_description = Column(String(255))
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    product_image_name = Column(String(255), nullable=False)
    product_image_path = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=0)
    created_date = Column(String(255))
    edited_date = Column(String(255))
    product_category_id = Column(Integer,
                                 ForeignKey(CategoryVO.category_id, onupdate="CASCADE"), nullable=False)
    product_subcategory_id = Column(Integer,
                                    ForeignKey(SubCategoryVO.subcategory_id, onupdate="CASCADE"), nullable=False)
