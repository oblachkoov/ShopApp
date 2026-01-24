from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


class UserRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        """
        Метод для работы с поль.

        Проверяет все операция с таблицы поль. в БД

        :param session: Асинхронная

        """
        self.session = session


    async def get_user_by_username(self, username: str) -> User | None:
        """
        Метод для получения поль.

        Проверяет поль. в БД по имени

        :param username: Имя поль.
        :return: не найдено если поль. нету

        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


    async def get_user_by_email(self, email: str) -> User | None:
        """
        Метод получения поль. по email

        Ищет поль. в БД по почте

        :param email: Почта поль.
        :return: ничего не найдено если поль. нету

        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


    async def create(self, username: str, email: str, fullname:str ,hashed_password: str, role: str = "client") -> User:
        """
        Метод создания нового поль.

        Создаёт нового поль. в БД

        :param username:  Имя поль.
        :param email: Почта поль.
        :param fullname: Полное имя поль.
        :param hashed_password: Хэшированный поль.
        :param role: Роль поль.

        """
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
        """
        Метод получение поль. по ИД

        Проверяет поль. по его ИД

        :param user_id: Идентификатор поль.
        :return: не найдено если поль. нету

        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_password(self, user_id: int, hashed_password: str) -> None:
        """
        Метод для обновления поль.

        Изменяет обновление поль.

        :param user_id: Идентификатор поль.
        :param hashed_password: Новый хэшированный пароль
        :return: Ничего

        """
        stmt = update(User).where(User.id == user_id).values(
            hashed_password=hashed_password,
        )
        await self.session.execute(stmt)
        await self.session.flush()


