from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.models import User


async def get_all_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def add_user(session: AsyncSession, data: dict):
    user = User(
        username=data["username"],
        telegram_id=data["telegram_id"],
    )
    session.add(user)
    await session.commit()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()


async def update_user(session: AsyncSession, telegram_id: int,  data: dict):
    query = update(User).where(User.id == telegram_id).values(
        username=data["username"],
    )
    await session.execute(query)
    await session.commit()


async def delete_user_by_id(session: AsyncSession, telegram_id: int):
    query = delete(User).where(User.id == telegram_id)
    await session.execute(query)
    await session.commit()


async def get_admins_user(session: AsyncSession):
    query = select(User).where(User.is_admin.is_(True))
    result = await session.execute(query)
    return result.scalars().all()
