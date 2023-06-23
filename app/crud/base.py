from typing import Generic, TypeVar, Optional, Any, Type
from tortoise.models import Model
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model : Type[ModelType]):
        self.model = model

    async def get(self, id :Any):
        return await self.model.filter(id = id).first()

    async def get_all(self, limit : int = 50):
        return await self.model.offset().limit(limit).all()

    async def create(self, obj_in : CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = await self.model.create(**obj_in_data)
        return db_obj

    async def update(self, obj_in : UpdateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = await self.model.update_from_dict(**obj_in_data)
        return db_obj
        
    async def remove(self, id :int) -> ModelType:
        obj = await self.model.filter(id=id).delete()
        return obj

    


    