from app.models import User, Role
from app.core.security import get_hashed_password
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app import crud
from app.core.config import settings

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

#get admin role
    def get_admin_role(self):
        return Role.filter(role = settings.ADMIN_ROLE).first()

# create admin 
    async def create(self, obj_in : UserCreate) -> User:
        admin_role = self.get_admin_role()
        db_obj = await User.create(
            **obj_in.dict(),
            school = await crud.school.get_by_domain(
                obj_in.email.split("@")[1]),
            hashed_password = get_hashed_password(obj_in.password),
            role = await User.role.add(admin_role)
        )
        return db_obj 

admin = CRUDUser(User)