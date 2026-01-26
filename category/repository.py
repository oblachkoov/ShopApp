from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from category.module import Categories
from category.schemas import CategoryCreate



class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: int)-> Categories | None:
        stmt = select(Categories).where(Categories.id == category_id)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category


    async def get_all(self, category_id: int)-> list | None:
        stmt = select(Categories).where(Categories.id == category_id)
        result = await self.session.execute(stmt)
        category = result.scalars().all()
        return category


    async def create(self, category: CategoryCreate) -> Categories:
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
        stmt = update(Categories).where(Categories.id == category_id).values(
            name=name,
            description=description
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete(self, category_id: int) -> None:
        stmt = delete(Categories).where(Categories.id == category_id)
        await self.session.execute(stmt)
        await self.session.flush()



