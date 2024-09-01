from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.core import db
from src.core.schemes import UserScheme
from .depends import get_repository
from .repository import Repository
from .schemes import TopScheme

router_v1 = APIRouter(prefix="/api/v1/pedometer", tags=["pedometer"])


@router_v1.get("/top", response_model=TopScheme)
async def get_top(repository: Repository = Depends(get_repository)
                  ) -> TopScheme:
    async with db.engine.begin() as conn:
        users = await repository.get_top(conn)
    scheme = TopScheme(users=[UserScheme.from_orm(user) for user in users])
    return scheme


@router_v1.get("/my_top", response_model=TopScheme)
async def get_my_top(user_id: PositiveInt, repository: Repository = Depends(get_repository)) -> TopScheme:
    async with db.engine.begin() as conn:
        users = await repository.get_my_top(conn, user_id)
    scheme = TopScheme(users=[UserScheme.from_orm(user) for user in users])
    return scheme


@router_v1.post("/set_step")
async def get_my_top(user_id: PositiveInt,
                     step: PositiveInt,
                     repository: Repository = Depends(get_repository)) -> None:
    async with db.engine.begin() as conn:
        await repository.set_step(conn, user_id, step)
