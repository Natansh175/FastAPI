from typing import Optional

from pydantic import BaseModel, Field


class CategoryDTO(BaseModel):
    category_name: str = Field(min_length=1)
    category_description: str = Field(min_length=1)
    category_count: int = Field(gt=0)

    class Config:
        from_attributes = True


class CategoryUpdateDTO(BaseModel):
    category_id: int = Field(gt=0)
    category_name: Optional[str] = Field(default=None, min_length=1)
    category_description: Optional[str] = Field(default=None, min_length=1)
    category_count: Optional[int] = Field(default=None, gt=0)

    class Config:
        from_attributes = True
