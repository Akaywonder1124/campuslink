from fastapi import APIRouter

from .routers import auth
from ..api_v1.routers import (users, school, interest, 
         event, admin)

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(school.router, prefix="/school", tags=["School"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin "])
api_router.include_router(interest.router, prefix="/interest", tags=["Interest"])
api_router.include_router(event.router, prefix="/event", tags=["event"])
# api_router.include_router(role.router, prefix="/role", tags=["Role"])

