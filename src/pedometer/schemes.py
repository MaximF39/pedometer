from pydantic import BaseModel

from src.core.schemes import UserScheme


class TopScheme(BaseModel):
    users: list[UserScheme]
