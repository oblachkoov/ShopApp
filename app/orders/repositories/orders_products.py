from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import Order

from app.orders.models import OrdersProducts
from app.orders.schemas import OrderProductsCreate
from app.products.routers import product


class OrderProductRepository:
    def __init__(
            self,
            session: AsyncSession,

    ):
        self.session = session

    async def create(
            self,
            products: list[OrderProductsCreate],
            order: Order
    ):
        order_products = [
            OrdersProducts(
                order_id=order.id,
                quantity=product.quantity,
                product_id=product.product_id,
                price=product.price
            )
            for product in products
        ]
        self.session.add_all(order_products)
        await self.session.flush()


    async def get(
            self,
            order: Order,
    ):
        stmt = select(OrdersProducts).where(OrdersProducts.order_id == order.id, OrdersProducts.products_id == product.id)
        result = await self.session.execute(stmt)
        products = result.scalars().all()
        return products

    async def get_all(
            self,
            order: Order
    ):
        stmt = select(OrdersProducts).where(OrdersProducts.order_id == order.id)
        result = await self.session.execute(stmt)
        products = result.scalars().all()
        return products


    async def delete(
            self,
            order: Order,
    ):
        stmt = delete(OrdersProducts).where(OrdersProducts.order_id == order.id)
        await self.session.execute(stmt)
        await self.session.flush()
