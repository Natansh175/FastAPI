from pydantic import BaseModel, Field
from typing import Optional


class SubCategoryDTO(BaseModel):
    subcategory_name: str = Field(min_length=1)
    subcategory_description: str = Field(min_length=1)
    subcategory_count: int = Field(gt=0)

    class Config:
        from_attributes = True


class UpdateSubCategoryDTO(BaseModel):
    subcategory_name: Optional[str] = None
    subcategory_description: Optional[str] = None
    subcategory_count: Optional[int] = None

    class Config:
        from_attributes = True

