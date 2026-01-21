from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


class UserRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session


    async def get_user(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


    async def create(self, username: str, email: str, fullname:str ,hashed_password: str, role: str = "client") -> User:
        stmt = insert(User).values(
            username=username,
            email=email,
            fullname=fullname,
            hashed_password=hashed_password,
            role=role,
        ).returning(User)
        result = await self.session.execute(stmt)
        await self.session.flush()
        user = result.scalars().first()
        return user


    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_password(self, user_id: int, hashed_password: str) -> None:
        stmt = update(User).where(User.id == user_id).values(
            hashed_password=hashed_password,
        )
        await self.session.execute(stmt)
        await self.session.flush()


