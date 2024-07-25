from pydantic import BaseModel


class RegisterDTO(BaseModel):
    first_name: str
    last_name: str
    gender: str
    address: str
    email: str
    password: str

    class Config:
        from_attributes = True
