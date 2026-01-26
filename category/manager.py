from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import PasswordServices
from category.module import Categories
from category.repository import CategoryRepository
from category.schemas import CategoryCreate, CategoryUpdate, CategoryDelete


class AuthManager:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
        self.category_repo = CategoryRepository(session)





    async def create_category(self, request: CategoryCreate) -> Categories:
        category = await self.category_repo.create_category(name=request.name, description=request.description)
        await self.session.commit()
        return category

    async def update_category(self, request: CategoryUpdate) -> Categories:
        category = await self.category_repo.update_category(category_id=request.id, name=request.name, description=request.description)
        await self.session.commit()
        return category


    async def delete_category(self, request: CategoryDelete) -> Categories:
        category = await self.category_repo.delete_category(category_id=request.id)
        await self.session.commit()
        return category




