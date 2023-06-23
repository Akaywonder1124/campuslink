from typing import Optional
from app.models import School
from app.crud.base import CRUDBase
from app.schemas.school import SchoolCreate, SchoolUpdate
from fastapi import HTTPException

class CRUDSchool(CRUDBase[School, SchoolCreate, SchoolUpdate]):
    def get_by_domain(self, domain : str) -> Optional[School]:
        school = School.get_or_none(school_domain = domain)
        return school

    def get_by_email(self, email : str) -> Optional[School]:
        return  School.filter(school_email = email ).first()

#Create school
    def create(self, obj_in : SchoolCreate) -> School:
        db_obj = School.create(
            school_email = obj_in.school_email,
            name = obj_in.name,
            school_domain = obj_in.school_email.split("@")[1],
            country = obj_in.country
        )
        
        return db_obj
        
#update user

    async def update(self, school_domain : str, updates: SchoolUpdate):
        school = await self.get_by_domain(school_domain)
        if not school:
            raise HTTPException(status_code=404, detail="school not found")
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(school, key, value)
        await school.save()
        

#delete interest

    async def delete(self, school_domain : str):
        interest = await self.get_by_domain(school_domain)
        if not interest:
            raise HTTPException(status_code=404, detail="interest not found")
        await interest.delete()

 
school = CRUDSchool(School)