from pydantic import BaseModel, Field
from typing import Optional


class ProductDTO(BaseModel):
    product_name: str = Field(min_length=1)
    product_description: str = Field(min_length=1)
    product_price: int = Field(gt=0)
    product_quantity: int = Field(gt=0)

    class Config:
        from_attributes = True


class UpdateProductDataDTO(BaseModel):
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_price: Optional[int] = None
    product_quantity: Optional[int] = None

    class Config:
        from_attributes = True
