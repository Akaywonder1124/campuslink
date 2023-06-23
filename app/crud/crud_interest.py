from app.models import Interest, User
from fastapi import HTTPException
from pydantic import EmailStr
from typing import Optional
from app.crud.base import CRUDBase
from app.schemas.interest import InterestCreate, InterestUpdate 
from app import crud 

class CRUDInterest(CRUDBase[Interest, InterestCreate, InterestUpdate]):

    #get interest
    def get_by_interest_name(self, interest_name : str) -> Optional[Interest]:
        return Interest.filter(interest_name=interest_name).first()

    #get user
    async def get_by_email(self, email : EmailStr) -> Optional[User]:
        user = await User.filter(email = email).first()
        if not user:
           raise HTTPException(status_code=400, detail="user not found")
        return user
        

#create interest

    async def create(self, obj_in : InterestCreate) -> Interest:
        db_obj =  await Interest.create(
            **obj_in.dict(),
            interest_admin =  await self.get_by_email(
                obj_in.interest_admin_email)
        )
        return db_obj

#update user

    async def update(self, interestname : str, updates: InterestUpdate):
        interest = await self.get_by_interest_name(interestname)
        if not interest:
            raise HTTPException(status_code=404, detail="interest not found")
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(interest, key, value)
        await interest.save()
        

#delete interest

    async def delete(self, interestname : str):
        interest = await self.get_by_interest_name(interestname)
        if not interest:
            raise HTTPException(status_code=404, detail="interest not found")
        await interest.delete()
        

interest = CRUDInterest(Interest)