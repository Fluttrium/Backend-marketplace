import uuid
from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)  # Ограничения на длину имени
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=128)  # Ограничения на длину пароля


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)  # Ограничения на длину имени
    last_name: str = Field(..., min_length=1, max_length=50)  # Ограничения на длину фамилии
