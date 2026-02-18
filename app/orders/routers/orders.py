from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv

from app.orders.dependencies import get_order_manager, get_order_or_404
from app.orders.filters import OrderFilter
from app.orders.managers.orders import OrderManager
from app.orders.models import Orders
from app.orders.schemas import OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/orders",
    tags=["order"]
)

@cbv(router)
class OrderRouter:
    manager: OrderManager = Depends(get_order_manager)



    @router.post("/")
    async def create(
            self,
            request: OrderCreate,
    ):
        await self.manager.create_order(request)


    @router.get("/")
    async def list(
            self,
            filters: OrderFilter = FilterDepends(OrderFilter),
    ):
        orders = await self.manager.get_all(filters)
        return orders


    @router.get("/{order_id}")
    async def detail(
            self,
            order: Orders = Depends(get_order_or_404)
    ):
        return order


    @router.put("/{order_id}")
    async def update(
            self,
            request: OrderUpdate,
            order: Orders = Depends(get_order_or_404)
    ):
        await self.manager.update_order(request, order)

    @router.delete("/{order_id}")
    async def delete(self, order: Orders = Depends(get_order_or_404)):
        await self.manager.delete_order(order)
