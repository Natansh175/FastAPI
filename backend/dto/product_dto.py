from pydantic import BaseModel
from typing import Optional


class ProductDTO(BaseModel):
    product_name: str
    product_description: str
    product_price: int
    product_quantity: int

    class Config:
        from_attributes = True


class UpdateProductDataDTO(BaseModel):
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_price: Optional[int] = None
    product_quantity: Optional[int] = None

    class Config:
        from_attributes = True
