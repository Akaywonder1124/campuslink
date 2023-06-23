from pydantic import BaseModel
from typing import Optional


class Msg(BaseModel):
    status : Optional[str] = None
    message: Optional[str] =None