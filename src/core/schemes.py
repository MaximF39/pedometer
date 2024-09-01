from pydantic import BaseModel


class UserScheme(BaseModel):
    id: int
    step: int

    class Config:
        from_attributes = True
