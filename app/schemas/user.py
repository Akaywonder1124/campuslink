from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    username : Optional[str] = None
    email : Optional[EmailStr] = None
    full_name : Optional[str] = None

class UserEmail(BaseModel):
    email : Optional[EmailStr] = None

class UserInterest(BaseModel):
    interest_name :str = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    full_name: str
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    profile_pic : Optional[str] = None
    about : Optional[str] = None
    date_of_birth : datetime = None
    

# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: Optional[int] = None
    about : Optional[str] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass