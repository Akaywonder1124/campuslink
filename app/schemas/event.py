from pydantic import BaseModel
from typing import Optional 


# Shared properties
class EventBase(BaseModel):
    event_name : Optional[str] = None
    description : Optional[str] = None
    venue : Optional[str] = None
    

#user interest field
class UserEvent(BaseModel):
    event_name : Optional[str] = None

# Properties to receive via API on creation
class EventCreate(EventBase):
    event_date : Optional[str] = None
    event_name : str = None
    description : str = None
    category : Optional[str] = None 

# Properties to receive via API on update
class EventUpdate(EventBase):
    event_name : Optional[str] = None
    description : Optional[str] = None

    class Config:
        orm_mode = True
# Additional properties to return via API
class Event(EventBase):
    event_category_id : Optional[int] = None
    pass