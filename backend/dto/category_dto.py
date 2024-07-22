from pydantic import BaseModel, constr
from typing import Optional

meaningful_string_pattern = r'[a-zA-Z0-9]'


class CategoryDTO(BaseModel):
    category_name: str
    category_description: str
    category_count: int

    class Config:
        from_attributes = True


class UpdateCategoryDTO(BaseModel):
    category_name: Optional[str] = None
    category_description: Optional[str] = None
    category_count: Optional[int] = None

    class Config:
        from_attributes = True
