from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, models, schemas
from app.core import config, security
from datetime import timedelta
from app.api import deps
from app.utils import (generate_password_reset_token,
        send_reset_password_email, verify_password_reset_token)




router = APIRouter()
@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate(username= form_data.username, 
                    password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")    
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id,
        expire_delta=access_token_expires, 
        scopes = form_data.scopes
        )
  
    if form_data.scopes:
        #check permission
        pass      

    return {
        "access_token" : access_token,
        "token_type" : "Bearer"
    }

@router.get("/login/get-user", response_model=schemas.User)
def get_current_user(current_user: models.User = Depends(deps.get_current_user)):
    return current_user

@router.get("/login/get-admin", response_model=schemas.User)
def get_super_admin(current_user: models.User = Depends(deps.get_super_admin)):
    return current_user

#password recovery

@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str):
    user = crud.user.get_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)

    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"message": "Password recovery email sent"}


#Reset Password
@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...)):

    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = security.get_hashed_password(new_password)
    user.hashed_password = hashed_password
    user.save()
    return {
        "status":"ok",
        "message": "Password updated successfully"
        }

