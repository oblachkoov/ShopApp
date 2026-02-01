from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import Product


class ProductRepository:
    def __init__(
            self,
            session: AsyncSession,

    ):
        self.session = session


    async def create(
            self,
            name: str,
            short_description: str,
            long_description: str,
            price: float,
            category_id: int,
    )-> Product:
        """
        Создание нового продукта.

        :param name: Название продукта
        :param short_description: Краткое описание продукта
        :param long_description: Полное описание продукта
        :param price: Цена продукта
        :param category_id: ID категории, к которой относится продукт
        :return: Созданный объект Product
        """
        stmt = insert(Product).values(
            name=name,
            short_description=short_description,
            long_description=long_description,
            price=price,
            category_id=category_id,
        ).returning(Product)
        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product


    async def delete(
            self,
            product_id: int,
    )-> None:
        """
        Удаление продукта по его ID.

        :param product_id: ID продукта
        :return: None
        """
        stmt = delete(Product).where(Product.id == product_id)
        await self.session.execute(stmt)
        await self.session.flush()


    async def update(
            self,
            product_id: int,
            name: str,
            short_description: str,
            long_description: str,
            price: float,
            category_id: int,
    )-> None:
        """
        Обновление данных продукта.

        :param product_id: ID продукта
        :param name: Новое название продукта
        :param short_description: Новое краткое описание
        :param long_description: Новое полное описание
        :param price: Новая цена продукта
        :param category_id: Новый ID категории
        :return: None
        """
        stmt = update(Product).where(Product.id == product_id).values(
            name=name,
            short_description=short_description,
            long_description=long_description,
            price=price,
            category_id=category_id,

        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def get_by_id(
            self,
            product_id: int,
    )-> Product:
        """
         Получение продукта по ID.

        :param product_id: ID продукта
        :return: Объект Product
        """
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product


    async def get_all(self):
        """
         Получение списка всех продуктов.

        :return: Список объектов Product
        """
        pass