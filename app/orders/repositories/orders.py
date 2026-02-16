from sqlalchemy import insert, delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import Order



class OrderRepository:
    def __init__(
            self,
            session: AsyncSession,

    ):
        self.session = session


    async def create(
            self,
            user_id: int,
            phone_number: str,
            address: str,
            comment: str,
            status,
    ) -> Order:
        stmt = insert(Order).values(
            user_id=user_id,
            phone_number=phone_number,
            address=address,
            comment=comment,
            status=status,
        ).returning(Order)
        result = await self.session.execute(stmt)
        await self.session.flush()
        order = result.scalars().first()
        return order



    async def delete(
            self,
            order_id: int,
    ) -> None:
        stmt = delete(Order).where(Order.id == order_id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def update(
            self,
            order_id: int,
            phone_number: str,
            address: str,
            comment: str,
            status: str,
    ) -> None:
        stmt = update(Order).where(Order.id == order_id).values(
            order_id=order_id,
            phone_number=phone_number,
            address=address,
            comment=comment,
            status=status,
        )
        await self.session.execute(stmt)
        await self.session.flush()



    async def get_order_by_id(
            self,
            order_id: int,
    )-> Order:

        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product


    async def get_all(self):
        pass


