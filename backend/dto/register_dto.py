from pydantic import BaseModel, Field


class RegisterDTO(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    gender: str = Field(..., min_length=3, max_length=10)
    address: str = Field(..., min_length=3, max_length=150)
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=5, max_length=20)

    class Config:
        from_attributes = True
