from typing import Optional
from pydantic import BaseModel, EmailStr



# Shared properties
class SchoolBase(BaseModel):
    name : Optional[str] = None
    school_email : Optional[EmailStr] = None
    country : Optional[str] = None

# Properties to receive via API on creation
class SchoolCreate(SchoolBase):
    name : str = None
    school_email : EmailStr = None
    country : str = None

# Properties to receive via API on update
class SchoolUpdate(SchoolBase):
    name: Optional[str] = None
    country : Optional[str] = None

# Properties to receive via API on update
class SchoolInDBBase(SchoolBase):
    id: Optional[int] = None
    school_domain : Optional[str] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class School(SchoolInDBBase):
    pass