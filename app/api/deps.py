from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from app.core.config import settings
from fastapi import Depends, HTTPException, status, Security
from pydantic import ValidationError
from jose import jwt
from app import schemas, crud, models
from app.core import security




oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "login/access-token", 
    scopes={"me" : "read current user",
    "admin" : "admin role",
    "creator" : "event_creator role",
    "interest_admin" : "interest_admin role"}
    )


async def get_current_user(
    security_scopes: SecurityScopes,
    token : str = Depends(oauth2_scheme)
    ):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(id=token_data.sub)
    if not user:
            raise HTTPException(status_code=404, detail="User not found")
    for scopes in security_scopes.scopes:
        if scopes not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
        
async def get_super_admin(
    current_user: models.User = Security((get_current_user), scopes=["me", "admin", "creator"])
):
    if current_user.role != settings.ADMIN_ROLE:
        raise HTTPException(status_code=400, detail="current user is not a super admin")
    return current_user
