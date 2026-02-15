from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import  AsyncSession

from app.products.models import ProductCharacteristics


class CharacteristicRepo:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def create_characteristic(
            self,
            name : str,
            value: str,
            product_id: int,
    )-> ProductCharacteristics:

        stmt = insert(ProductCharacteristics).values(
            name=name,
            value=value,
            product_id=product_id,
        ).returning(ProductCharacteristics)
        result = await self.session.execute(stmt)
        await self.session.flush()
        product_characteristic = result.scalars().first()
        return product_characteristic


    async def get_characteristic_by_id(
            self,
            characteristic_id: int,
            product_id,
    )-> ProductCharacteristics:
        stmt = select(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id, ProductCharacteristics.product_id == product_id)
        result = await self.session.execute(stmt)
        product_characteristic = result.scalar_one_or_none()
        return product_characteristic


    async def get_all(
            self,
            product_id
    ):
        stmt = select(ProductCharacteristics).where(
            ProductCharacteristics.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def update_characteristic(
            self,
            characteristic_id: int,
            name: str,
            value: str,
    ) -> None:
        stmt = update(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id).values(
            name=name,
            value=value,
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete_characteristic(
            self,
            characteristic_id: int,
    )-> None:
        stmt = delete(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id)
        await self.session.execute(stmt)
        await self.session.flush()


