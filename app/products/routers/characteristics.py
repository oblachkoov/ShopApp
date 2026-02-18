from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import is_admin
from app.products.dependencies import (get_characteristics_manager,get_product_or_404,get_characteristics_or_404)
from app.products.managers.characteristic_manager import CharacteristicManager
from app.products.models import Product, ProductCharacteristics
from app.products.schemas import (ProductCharacteristicsCreate, ProductCharacteristicsUpdate)

router = APIRouter(
    prefix="/products/{product_id}/characteristics",
    tags=["characteristics"]
)


@cbv(router)
class CharacteristicsRouter:
    manager: CharacteristicManager = Depends(get_characteristics_manager)


    @router.post("/", dependencies=[Depends(is_admin)])
    async def create(
            self,
            request: ProductCharacteristicsCreate,
            product: Product = Depends(get_product_or_404),
    ):
        return await self.manager.create_characteristic(
            request=request,
            product_id=product.id
        )


    @router.get("/")
    async def list(
            self,
            product: Product = Depends(get_product_or_404),
    ):
        return await self.manager.get_all_by_product(product.id)

    @router.get("/{characteristic_id}")
    async def detail(
            self,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        return characteristic


    @router.put("/{characteristic_id}", dependencies=[Depends(is_admin)])
    async def update(
            self,
            request: ProductCharacteristicsUpdate,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        await self.manager.update_characteristic(
            characteristic_id=characteristic.id,
            request=request
        )

    @router.delete("/{characteristic_id}", dependencies=[Depends(is_admin)])
    async def delete(
            self,
            characteristic: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        await self.manager.delete_characteristic(characteristic.id)
