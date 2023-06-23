from fastapi import APIRouter, Depends, HTTPException
from app import schemas, crud, models
from typing import List
from app.api import deps
import datetime

router =APIRouter()

#get all event by Interest
@router.get("/get-by-interest/{interest_name}", response_model=List[schemas.Event])
async def get_interest(interest_name : str):
    interest = await crud.interest.get_by_interest_name(interest_name)
    if not interest:
        raise HTTPException(status_code=400, detail="Interest not found")
    events = await models.Event.filter(event_category = interest.id).all()
    return events

#get all event by Time
@router.get("/get-by-time{time}", response_model=List[schemas.Event])
async def get_event_time(time : str):
    events = await models.Event.filter(event_date = time).all()
    return events

#get all event by date
@router.get("/get-by-date{date}", response_model=List[schemas.Event])
async def get_event_date(date : str):
    events = await models.Event.filter(event_date = date ).all()
    return events

#create event
@router.post("/create", response_model=schemas.Event)
async def create_event(
    event_in : schemas.EventCreate,
    event_creator : models.User = Depends(deps.get_current_user)
    ):
    event_name = await crud.event.get_by_event_name(
                            event_in.event_name)
    if event_name:
        raise HTTPException(status_code=400, detail="event already exist")
    event = await crud.event.create(event_in, event_creator)
    return event

#update event


#delete event