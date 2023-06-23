from app.models import Interest, Event, User
from fastapi import HTTPException
from pydantic import EmailStr
from typing import Optional
from app.crud.base import CRUDBase
from app.schemas.event import (EventCreate, EventUpdate)
from app import crud 

class CRUDevent(CRUDBase[Event, EventCreate, EventUpdate]):

    #get interest
    def get_by_event_name(self, event_name : str) -> Optional[Event]:
        return Event.filter(event_name=event_name).first()

    def get_interest_by_name(self, interest_name : str) -> Optional[Interest]:
        interest = Interest.filter(interest_name=interest_name).first()
        if not interest:
            raise HTTPException(status_code=404, detail="Interest not found")
        else:
            return interest
            

#create event

    async def create(self, obj_in : EventCreate, event_creator) -> Event:
        db_obj =  await Event.create(
            **obj_in.dict(),
            event_creator =  event_creator,
            event_category = await self.get_interest_by_name(obj_in.category)
        )
        return db_obj

#update user

    async def update(self, event_name : str, updates: EventUpdate):
        event = await self.get_by_event_name(event_name)
        if not event:
            raise HTTPException(status_code=404, detail="event not found")
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        await event.save()
        

#delete interest

    async def delete(self, event_name : str):
        event = await self.get_by_event_name(event_name)
        if not event:
            raise HTTPException(status_code=404, detail="event not found")
        await event.delete()
        

event = CRUDevent(Event)