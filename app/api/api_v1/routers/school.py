from  fastapi import APIRouter, HTTPException
from app import schemas, crud



router = APIRouter()

@router.post("/register", response_model=schemas.School)
async def register_school(school_in : schemas.SchoolCreate):
    school = await crud.school.get_by_email(school_in.school_email)
    if school:
        raise HTTPException(status_code=400, detail="school already exist")
    else:
        school = await crud.school.create(school_in)
        return school
    #send admin registration endpoint to email

@router.patch("/update/{school_domain}", response_model=schemas.Msg)
async def update_school(school_domain : str, school_in : schemas.SchoolUpdate):
    school_db = await crud.school.get_by_domain(school_domain)
    if not school_db:
        raise HTTPException(status_code=404, detail="school not found")
    school = await crud.school.update(school_db.school_domain, school_in)
    return {"status" : "ok",
            "message" : "school updated successfully"}

@router.delete("/delete/{school_domain}",  response_model=schemas.Msg)
async def delete_school(school_domain : str):
    school_db = await crud.school.get_by_domain(school_domain)
    if not school_db:
        raise HTTPException(status_code=404, detail="school not found")
    school = await crud.school.delete(school_domain)
    return {"status" : "ok",
            "message" : f"{school_db.name} has been deleted"}
