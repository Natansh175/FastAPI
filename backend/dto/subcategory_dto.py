from pydantic import BaseModel, Field
from typing import Optional


class SubCategoryDTO(BaseModel):
    subcategory_name: str
    subcategory_description: str
    subcategory_count: int

    class Config:
        from_attributes = True


class UpdateSubCategoryDTO(BaseModel):
    subcategory_name: Optional[str] = None
    subcategory_description: Optional[str] = None
    subcategory_count: Optional[int] = None

    class Config:
        from_attributes = True

