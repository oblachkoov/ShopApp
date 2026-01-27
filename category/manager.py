from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from category.module import Categories
from category.repository import CategoryRepository
from category.schemas import CategoryCreate, CategoryUpdate, CategoryDelete


class CategoryManager:
    def __init__(
            self,
            session: AsyncSession
    ):
        """
        Метод  для работы с категориями

        :param session: Асинхронная сессия
        """
        self.session = session
        self.category_repo = CategoryRepository(session)


    async def get_category(self, category_id: int)-> Categories | None:
        """
        Метод для получения категории

        Получает категорию по ID из БД

        :param category_id: Идентификатор категории
        :return: Объект категории или None, если категория не найдена
        """
        return await self.category_repo.get_by_id(category_id)


    async def get_all_categories(self)-> list[Categories]:
        """
        Метод для получения списка категории

        Получает все  категории  по ID из БД

        :return: Список категории
        """
        stmt = select(Categories)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()
        return categories


    async def create_category(self, request: CategoryCreate) -> Categories:
        """
        Метод для создания категории

        Создаёт новую категорию в базе данных

        :param request: Pydantic модель CategoryCreate
        :return: Объект созданной категории
        """
        category = await self.category_repo.create(request)
        await self.session.commit()
        return category


    async def update_category(self, request: CategoryUpdate) -> None:
        """
        Метод для обновления категории

        Обновляет данные категории в БД

        :param request: Pydantic модель CategoryUpdate
        :return: Ничего
        """
        await self.category_repo.update(
            category_id=request.id,
            name=request.name,
            description=request.description,
        )
        await self.session.commit()



    async def delete_category(self, request: CategoryDelete) -> None:
        """
        Метод для удаления категории

        Удаляет категорию из БД по ID

        :param request: Pydantic модель CategoryDelete
        :return: Ничего
        """
        await self.category_repo.delete(request.id)
        await self.session.commit()



