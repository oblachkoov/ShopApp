from typing import List

from sqlalchemy.testing.pickleable import Order

from app.auth.models import User
from app.core.exceptions import NotFound
from app.orders.repositories.orders import OrderRepository
from app.orders.repositories.orders_products import OrderProductRepository
from app.orders.schemas import OrderCreate


class OrderManager:
    def __init__(self, session):
        self.session = session
        self.repo = OrderRepository(self.session)
        self.order_products_repo = OrderProductRepository(self.session)

    async def create(
            self,
            request: OrderCreate,
            user: User,
    ):
        order = await self.repo.create(
            user_id=user.id,
            **request.model_dump(exclude={"products"}),
        )
        await self.order_products_repo.create(
            request.products,
            order=order,
        )
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_by_id(self, order_id: int) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise NotFound("Order not found")
        return order

    async def delete(
            self,
            order: Order,
    ):
        await self.repo.delete(order)

    async def list(self, filters) -> List[Order]:
        orders = await self.repo.get_all(filters)
        return orders