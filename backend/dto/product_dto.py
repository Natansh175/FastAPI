from pydantic import BaseModel, Field
from typing import Optional


class ProductDTO(BaseModel):
    product_category_id: int = Field(gt=0)
    product_subcategory_id: int = Field(gt=0)
    product_name: str = Field(min_length=1, max_length=50)
    product_description: str = Field(min_length=1, max_length=100)
    product_price: int = Field(gt=0)
    product_quantity: int = Field(gt=0)

    class Config:
        from_attributes = True


class ProductDataUpdateDTO(BaseModel):
    product_id: int = Field(gt=0)
    product_name: Optional[str] = Field(default=None, min_length=1)
    product_description: Optional[str] = Field(default=None, min_length=1)
    product_price: Optional[int] = Field(default=None, gt=0)
    product_quantity: Optional[int] = Field(default=None, gt=0)

    class Config:
        from_attributes = True
