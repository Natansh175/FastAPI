from pydantic import BaseModel
from typing import Optional


class CategoryDto(BaseModel):
    category_name: str
    category_description: str
    category_count: int

    class Config:
        from_attributes = True


class UpdateCategoryDto(BaseModel):
    category_name: Optional[str] = None
    category_description: Optional[str] = None
    category_count: Optional[int] = None

    class Config:
        from_attributes = True
