from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.orders.managers.orders import OrderManager




async def get_order_manager(
    session: AsyncSession = Depends(get_db)
):

    return OrderManager(session)



async def get_order_or_404(
    order_id: int,
    manager: OrderManager = Depends(get_order_manager()),
):

    return await manager.get_order(order_id)