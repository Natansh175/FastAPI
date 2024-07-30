from typing import Optional

from pydantic import BaseModel, Field


class SubCategoryDTO(BaseModel):
    subcategory_category_id: int = Field(gt=0)
    subcategory_name: str = Field(min_length=1, max_length=50)
    subcategory_description: str = Field(min_length=1, max_length=100)
    subcategory_count: int = Field(gt=0)

    class Config:
        from_attributes = True


class SubCategoryUpdateDTO(BaseModel):
    subcategory_id: int = Field(gt=0)
    subcategory_name: Optional[str] = Field(default=None, min_length=1)
    subcategory_description: Optional[str] = Field(default=None, min_length=1)
    subcategory_count: Optional[int] = Field(default=None, gt=0)

    class Config:
        from_attributes = True
