from typing import Optional, List
from pydantic import BaseModel, Field, validator
import re  # Added this import for regex validation

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str  # Changed from EmailStr to regular string with custom validation
    full_name: Optional[str] = None

    @validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("must be a valid email address")
        return v.lower()  # Convert to lowercase for consistency

class UserCreate(UserBase):
    password: str

class User(UserBase):
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class ItemBase(BaseModel):
    name: str = Field(..., example="Widget")
    description: Optional[str] = Field(None, example="A very useful widget")
    price: float = Field(..., gt=0, example=35.4)

class ItemCreate(ItemBase):
    tax: Optional[float] = Field(None, example=3.2)

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Widget")
    description: Optional[str] = Field(None, example="An updated description")
    price: Optional[float] = Field(None, gt=0, example=40.0)
    tax: Optional[float] = Field(None, example=4.0)

class Item(ItemBase):
    id: int
    tax: Optional[float]
    owner: str

    class Config:
        orm_mode = True