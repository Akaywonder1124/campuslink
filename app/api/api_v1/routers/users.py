from fastapi import APIRouter, HTTPException,  Depends
from app import schemas, crud, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.User)
async def get_user(
        user_db : models.User = Depends(deps.get_current_user)
        ):
    users = await crud.user.get(id=user_db.id)
    return users


@router.post("/register", response_model=schemas.User)
async def user_registration(user_in : schemas.UserCreate):
    username = await crud.user.get_by_username(user_in.username)
    if username:
        raise HTTPException(status_code=400, detail="username already exist")
    email = await crud.user.get_by_email(user_in.email)
    if email:
        raise HTTPException(status_code=400, detail="email already exist")
    school_domain = user_in.email.split("@")[1]
    school = await crud.school.get_by_domain(school_domain)
    if school == None:
        raise HTTPException(status_code=400, detail="school is not registered")
    user = await crud.user.create(user_in)
    return user

#update account
@router.patch("/update", response_model=schemas.Msg)
async def update_user(
    user_in : schemas.UserUpdate,
    user_db: models.User = Depends(deps.get_current_user)):
    user = await crud.user.update(user_db.username, user_in)
    return {
        "status" : "ok",
        "message" : "user updated succesfully"}
    


#delete account
@router.delete("/delete", response_model=schemas.Msg)
async def delete_account(user_db : models.User  = Depends(deps.get_current_user)):
    user = await crud.user.delete(user_db.username)
    return {"status" : "ok",
    "message" : "user account deleted"}

#choose interest
@router.post("/choose-interest", response_model=schemas.Msg)
async def choose_interest(
        user_interest : schemas.UserInterest,
        user_db : models.User = Depends(deps.get_current_user)):
        interest = await crud.interest.get_by_interest_name(
                    user_interest.interest_name)
        if not interest:
            raise HTTPException(status_code=400, detail="Interest is not available")
        await user_db.interest.add(interest)
        user_db.save()
        return {
            "status" : "ok",
            "message" : "Interest successfully added"}    

#delete interest
@router.delete("/remove-interest/{interest_name}", response_model=schemas.Msg)
async def remove_interest(
    user_interest : schemas.UserInterest,
    user_db : models.User = Depends(deps.get_current_user)):
    interest = await crud.interest.get_by_interest_name(
                    user_interest.interest_name)
    if not interest:
        raise HTTPException(status_code=400, detail="Interest is not available")
    await user_db.interest.remove(interest)
    user_db.save()
    return {"status" : "ok",
            "message" : "Interest removed successfully"}

#choose interest
@router.post("/choose-event", response_model=schemas.Msg)
async def choose_event(
        user_event : schemas.UserEvent,
        user_db : models.User = Depends(deps.get_current_user)):
        event = await crud.event.get_by_event_name(
                    user_event.event_name)
        if not event:
            raise HTTPException(status_code=404, detail="Event is not available")
        await user_db.event.add(event)
        user_db.save()
        return {
            "status" : "ok",
            "message" : "Event successfully added"} 

#delete interest
@router.delete("/remove-event/{event_name}", response_model=schemas.Msg)
async def remove_event(
    user_event : schemas.UserEvent,
    user_db : models.User = Depends(deps.get_current_user)):
    event = await crud.event.get_by_event_name(user_event.event_name)
    if not event:
        raise HTTPException(status_code=404, detail="Event is not available")
    await user_db.event.remove(event)
    user_db.save()
    return {"status" : "ok",
            "message" : "Event removed successfully"}