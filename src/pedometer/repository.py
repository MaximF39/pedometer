from typing import TypeVar

from pydantic import BaseModel, PositiveInt
from sqlalchemy import select, CursorResult, union_all, update
from sqlalchemy.ext.asyncio import AsyncConnection

from core.models import User

type_scheme = TypeVar("scheme", bound=BaseModel)


class Repository:
    async def get_top(self, conn: AsyncConnection) -> CursorResult[tuple[User]]:
        users = await conn.execute(select(User).order_by(User.step.desc()).limit(10))
        return users

    async def get_my_top(self, conn: AsyncConnection, user_id: PositiveInt) -> CursorResult[tuple[User]]:
        user_step = await conn.scalar(select(User.step).where(User.id == user_id))

        # Create a query that selects the top 5 users with a higher step value than the given user
        top_users_query = select(User).where(User.step >= user_step).order_by(User.step.desc()).limit(5)

        # Create a query that selects the bottom 5 users with a lower step value than the given user
        bottom_users_query = select(User).where(User.step <= user_step).order_by(User.step).limit(5)

        # Combine the queries using union_all
        query = union_all(top_users_query, bottom_users_query)

        # Execute the query and extract the User objects from the result set
        users = await conn.execute(query)

        return users

    async def set_step(self, conn: AsyncConnection, user_id: PositiveInt, step: int) -> None:
        stmt = update(User).where(User.id == user_id).values(step=step)
        await conn.execute(stmt)
