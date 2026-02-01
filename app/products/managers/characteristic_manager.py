from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import ProductCharacteristics
from app.products.repositories.characteristic_repo import CharacteristicRepo
from app.products.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate


class CharacteristicManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.characteristic_repo = CharacteristicRepo(session)

    async def get_characteristic(self, characteristic_id: int) -> ProductCharacteristics | None:
        return await self.characteristic_repo.get_characteristic_by_id(characteristic_id)


    async def create_characteristic(self, request: ProductCharacteristicsCreate) -> ProductCharacteristics:
        characteristic = await self.characteristic_repo.create_characteristic(
            name=request.name,
            value=request.value,
            product_id=request.product_id
        )
        await self.session.commit()
        return characteristic

    async def update_characteristic(self, request: ProductCharacteristicsUpdate) -> None:
        await self.characteristic_repo.update_characteristic(
            characteristic_id=request.id,
            name=request.name,
            value=request.value
        )
        await self.session.commit()

    async def delete_characteristic(self, characteristic_id: int) -> None:
        await self.characteristic_repo.delete_characteristic(characteristic_id)
        await self.session.commit()
