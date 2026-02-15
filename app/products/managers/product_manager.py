from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import Product
from app.products.repositories.product_repo import ProductRepository
from app.products.schemas import ProductCreate, ProductUpdate, ProductNotFound


class ProductManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)


    async def get_product(self, product_id: int) -> Product:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFound("Product not found")
        return product


    async def create_product(self, request: ProductCreate) -> Product:
        product = await self.product_repo.create(
            name=request.name,
            short_description=request.short_description,
            long_description=request.long_description,
            price=request.price,
            category_id=request.category_id
        )
        await self.session.commit()
        return product

    async def update_product(self, request: ProductUpdate, product: Product) -> None:
        await self.product_repo.update(
            product,
            **request.model_dump()
        )
        await self.session.commit()


    async def delete_product(self, product: Product) -> None:
        await self.product_repo.delete(product)
        await self.session.commit()


