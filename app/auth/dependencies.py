from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import AuthManager
from app.core.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db)
):
    """
    Функция для возрата текущего поль.

    :param token: Токен из Headers(Authorization)
    :param session: Асинх. Сессия из зависимости get_db
    :return: Моделька поль.
    """

    manager = AuthManager(session)
    user = await manager.get_me(token)
    return user


async def get_auth_manager(
        session: AsyncSession = Depends(get_db)
):
    return AuthManager(session)
