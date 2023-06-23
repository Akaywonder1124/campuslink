from pydantic import BaseModel, EmailStr
from typing import Optional


# Shared properties
class InterestBase(BaseModel):
    interest_name : Optional[str] = None
    description : Optional[str] = None

#user interest field
class UserInterest(BaseModel):
    interest_name : Optional[str] = None

# Properties to receive via API on creation
class InterestCreate(InterestBase):
    interest_name : str = None
    description : str = None
    interest_admin_email: EmailStr = None

# Properties to receive via API on update
class InterestUpdate(InterestBase):
    interest_name : Optional[str] = None
    description : Optional[str] = None
    interest_admin : Optional[int] = None

    class Config:
        orm_mode = True
# Additional properties to return via API
class Interest(InterestBase):
    pass