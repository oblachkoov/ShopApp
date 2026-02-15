from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import ProductCharacteristics, Product
from app.products.repositories.characteristic_repo import CharacteristicRepo
from app.products.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate, CharacteristicNotFound


class CharacteristicManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.characteristic_repo = CharacteristicRepo(session)


    async def get_characteristic(self, product: Product, characteristic_id: int) -> ProductCharacteristics:
        characteristic = await self.characteristic_repo.get_characteristic_by_id(characteristic_id, product.id)
        if not characteristic:
            raise CharacteristicNotFound(
                "Characteristic not found",
            )
        return characteristic


    async def get_all_characteristic(
            self,
            product: Product,
    ):
        characteristics = await self.characteristic_repo.get_all(product.id)
        return characteristics


    async def create_characteristic(self, request: ProductCharacteristicsCreate, product: Product) -> ProductCharacteristics:
        characteristic = await self.characteristic_repo.create_characteristic(
            **request.model_dump(),
            product_id=product.id
        )
        await self.session.commit()
        return characteristic


    async def update_characteristic(self, request: ProductCharacteristicsUpdate, characteristic: ProductCharacteristics) -> None:
        await self.characteristic_repo.update_characteristic(
            characteristic,
            **request.model_dump(),
        )
        await self.session.commit()


    async def delete_characteristic(self, characteristic: ProductCharacteristics) -> None:
        await self.characteristic_repo.delete_characteristic(characteristic)
        await self.session.commit()
