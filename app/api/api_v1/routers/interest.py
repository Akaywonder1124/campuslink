from fastapi import APIRouter, Depends, HTTPException
from app import schemas, crud, models
from typing import List



router =APIRouter()

#get all interest

@router.get("/get-interests", response_model=List[schemas.Interest])
async def get_all_interests():
    interest = await models.Interest.all()
    return interest


#create interest

@router.post("/create", response_model=schemas.Interest)
async def create_interest(
    interest_in : schemas.InterestCreate
    ):
    interest_name = await crud.interest.get_by_interest_name(interest_in.interest_name)
    if interest_name:
        raise HTTPException(status_code=400, detail="Interest already exist")
    interest = await crud.interest.create(interest_in)
    return interest

#update interest
@router.patch("/update/{interest_name}")
async def update_interest(
    interest_name : str,
    interest_in : schemas.InterestUpdate
):
    interest_db = await crud.interest.get_by_interest_name(interest_name)
    if not interest_db:
        raise HTTPException(status_code=400, detail="Interest not found")
    interest = await crud.interest.update(
                interest_db.interest_name,
                interest_in)
    return {"message" : "Interest updated successfully"}

#delete interest
@router.delete("/delete/{interest_name}")
async def delete_interest(interest_name : str):
    del_interest = await crud.interest.delete(interest_name)
    return {"message" : f"{interest_name} deleted"}
   