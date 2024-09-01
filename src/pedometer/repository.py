from typing import TypeVar

from pydantic import BaseModel, PositiveInt
from sqlalchemy import select, CursorResult, union_all, update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.core.models import User

type_scheme = TypeVar("type_scheme", bound=BaseModel)


class Repository:
    async def get_top(self, conn: AsyncConnection) -> CursorResult[tuple[User]]:
        users = await conn.execute(select(User).order_by(User.step.desc()).limit(10))
        return users

    async def get_my_top(self, conn: AsyncConnection, user_id: PositiveInt) -> CursorResult[tuple[User]]:
        user_step = await conn.scalar(select(User.step).where(User.id == user_id))
        top_users_query = select(User).where(User.step >= user_step).order_by(User.step.desc()).limit(5)
        bottom_users_query = select(User).where(User.step <= user_step).order_by(User.step).limit(5)
        query = union_all(top_users_query, bottom_users_query)
        users = await conn.execute(query)
        return users

    async def set_step(self, conn: AsyncConnection, user_id: PositiveInt, step: int) -> None:
        stmt = update(User).where(User.id == user_id).values(step=step)
        await conn.execute(stmt)
