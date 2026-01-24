from app.core.session import async_session


async def get_db():
    """
    Функция для создания асин. сессии

    :return: None
    """
    async with async_session() as session:
        yield session

