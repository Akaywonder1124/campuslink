from fastapi import APIRouter, HTTPException
from app import schemas, crud
from app.core.config import settings
# from .role import get_role

router = APIRouter()


@router.post("/register", response_model=schemas.User)
async def admin_registration(user_in : schemas.UserCreate):
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
    user = await crud.admin.create(user_in)
    return user

#assign category admin
@router.post("/assign-subadmin", response_model=schemas.Msg)
async def assign_subadmin(category_admin : schemas.UserEmail ):
    user = await crud.user.get_by_email(category_admin.email)
    role = await get_role(settings.INTEREST_ADMIN_ROLE)
    if user:
        await user.role.add(role)
        user.save()
        #notify user via email
        return {"status": "ok",
            "message" : f"{user.username} is now an Interest admin"}
    else:
        raise HTTPException(status_code=400, detail="user not found")

#assign category admin
@router.post("/remove-subadmin", response_model=schemas.Msg)
async def remove_subadmin(category_admin : schemas.UserEmail ):
    user = await crud.user.get_by_email(category_admin.email)
    role = await get_role(settings.INTEREST_ADMIN_ROLE)
    if user:
        await user.role.remove(role)
        user.save()
        #notify user via email
        return {"status": "ok",
            "message" : f"{user.username} is no longer an Interest admin"}
    else:
        raise HTTPException(status_code=400, detail="user not found")