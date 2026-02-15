from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import ProductReview


class ReviewRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def create_review(
            self,
            user_id: int,
            product_id: int,
            message: str,
            grade: int
    )-> ProductReview:

        stmt = insert(ProductReview).values(
            user_id=user_id,
            product_id=product_id,
            message=message,
            grade=grade,
        ).returning(ProductReview)
        result = await self.session.execute(stmt)
        await self.session.flush()
        product_review = result.scalars().first()
        return product_review

    async def get_review_by_id(
            self,
            review_id,
            product_id
    )-> ProductReview:
        stmt = select(ProductReview).where(ProductReview.id == review_id, ProductReview.product_id==product_id)
        result = await self.session.execute(stmt)
        product_review = result.scalar_one_or_none()
        return product_review


    async def update_review(
            self,
            review_id: int,
            message: str,
            grade: int
    ) -> None:
        stmt = update(ProductReview).where(ProductReview.id == review_id).values(
            message=message,
            grade=grade,
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete_review(
            self,
            review_id: int
    )-> None:
        stmt = delete(ProductReview).where(ProductReview.id == review_id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_all(self):
        pass
