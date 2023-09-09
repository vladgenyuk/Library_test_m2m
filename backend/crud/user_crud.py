from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_

from backend.models.user import Reader


class CrudUser:

    async def get_user_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(Reader).where(Reader.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_users(
            self,
            session: AsyncSession,
    ):
        stmt = select(Reader)
        result = await session.execute(stmt)
        return [dict(r._mapping)['Reader'] for r in result]

    async def login_user(
            self,
            session: AsyncSession,
            email: str,
            first_name: str
    ):
        stmt = select(Reader).where(and_(Reader.email == email, Reader.first_name == first_name))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def register_user(
            self,
            session: AsyncSession,
            user_data: dict
    ):
        reader = Reader(**user_data)
        session.add(reader)
        await session.flush()
        await session.commit()
        return reader


user = CrudUser()
