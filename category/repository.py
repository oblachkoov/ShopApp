from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from category.module import Categories
from category.schemas import CategoryCreate



class CategoryRepository:
    def __init__(self, session: AsyncSession):
        """
        Метод для работы с категориями

        :param session: Асинхронная сессия
        """
        self.session = session

    async def get_by_id(self, category_id: int)-> Categories | None:
        """
        Метод для получения категории

        Ищет категорию в БД по иденфикатеру

        :param category_id: Иденфикатор категории
        :return: Категори или None, если категория не найдена
        """
        stmt = select(Categories).where(Categories.id == category_id)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category


    async def get_all(self, category_id: int)-> list | None:
        """
        Метод для получения списка категории

        Получает список  категорию в БД

        :param category_id: Иденфикатор категории
        :return: Список категории
        """
        stmt = select(Categories).where(Categories.id == category_id)
        result = await self.session.execute(stmt)
        category = result.scalars().all()
        return category


    async def create(self, category: CategoryCreate) -> Categories:
        """
        Метод для создания категории

        Создаёт новую категория в БД

        :param category_id: Pydantic модель CategoryCreate
        :return: Объект созданной категорий
        """
        stmt = insert(Categories).values(
            name=category.name,
            description=category.description,
        ).returning(Categories)
        result = await self.session.execute(stmt)
        await self.session.flush()
        category = result.scalars().first()
        return category



    async def update(
            self,
            category_id: int,
            name: str,
            description: str
    ) -> Categories:
        """
        Метод для обновление  категории

        Обновляет название и описание категории в БД

        :param category_id: Идентификатор категории
        :param name: Новое название категории
        :param description: Новое описание категории
        :return: Обновлённый объект категории
        """
        stmt = update(Categories).where(Categories.id == category_id).values(
            name=name,
            description=description
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete(self, category_id: int) -> None:
        """
        Метод удаления категории

        Удаляет категорию из БД по ID

        :param category_id: Идентификатор категории
        :return: Ничего
        """
        stmt = delete(Categories).where(Categories.id == category_id)
        await self.session.execute(stmt)
        await self.session.flush()



