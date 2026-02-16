from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.models import OrdersProducts
from app.products.models import Product


class OrderProductRepository:
    def __init__(
            self,
            session: AsyncSession,

    ):
        self.session = session

    async def create(
            self,
            order_id: int,
            quantity: int,
            product_id: int,
            price: float,
    ) -> OrdersProducts:
        stmt = insert(Product).values(
            order_id=order_id,
            quantity=quantity,
            product_id=product_id,
            price=price,
        ).returning(OrdersProducts)
        result = await self.session.execute(stmt)
        await self.session.flush()
        order_product = result.scalars().first()
        return order_product

    async def delete(
            self,
            order_product: OrdersProducts,
    ) -> None:
        await self.session.delete(order_product)
        await self.session.flush()

    async def update(
            self,
            order_product: OrdersProducts,
            quantity: int,
            product_id: int,
            price: float,
            order_id: int,
    ) -> None:
        order_product.order_id = order_id
        order_product.quantity = quantity
        order_product.product_id = product_id
        order_product.price = price
        await self.session.update(order_product)
        await self.session.flush()
        

    async def get_by_id(
            self,
            order_id: int,
    ) -> OrdersProducts:
        stmt = select(Product).where(OrdersProducts.order_id == order_id)
        result = await self.session.execute(stmt)
        order_product = result.scalar_one_or_none()
        return order_product


    async def get_all(self):
        pass