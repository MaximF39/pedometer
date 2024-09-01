from pydantic import BaseModel

from core.schemes import UserScheme


class TopScheme(BaseModel):
    users: list[UserScheme]
