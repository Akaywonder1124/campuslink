from typing import  Optional
from pydantic import EmailStr
from fastapi import HTTPException
from app.models import User, Role
from app.core.security import get_hashed_password, verify_password
from app.core.config import settings
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app import crud 

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, email : EmailStr) -> Optional[User]:
        return  User.filter(email = email).first()
        
    def get_by_username(self, username : str) -> Optional[User]:
        return User.filter(username=username).first()

# create user 
    async def create(self, obj_in : UserCreate) -> User:
        db_obj = await User.create(
            school = await crud.school.get_by_domain(
                obj_in.email.split("@")[1]),
            email = obj_in.email,
            hashed_password = get_hashed_password(obj_in.password),
            full_name = obj_in.full_name,
            username = obj_in.username
        )
        return db_obj 

#update user

    async def update(self, username : str, updates: UserUpdate):
        from datetime import datetime
        from dateutil.parser import parse
        user = await self.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, datetime.utcnow())
            print(type(getattr(user, key)))
        await user.save()

#delete account

    async def delete(self, username : str):
        user = await self.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        await user.delete()

# authenticate user
    async def authenticate(self, username, password):
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

# get active user


    
user = CRUDUser(User)