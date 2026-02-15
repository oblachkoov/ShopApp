from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import ProductReview, Product
from app.products.repositories.review_repo import ReviewRepository
from app.products.schemas import ProductReviewCreate, ProductReviewUpdate


class ReviewManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.review_repo = ReviewRepository(session)

    async def get_review(
            self,
            product: Product,
            review_id: int
    ) -> ProductReview:
        review = self.review_repo.get_review_by_id(review_id, product.id)
        if not review:
            return await self.review_repo.get_review_by_id(review_id)


    async def create_review(
            self,
            request: ProductReviewCreate,
            user,
            product: Product
    ) -> ProductReview:
        review = await self.review_repo.create_review(
            **request.model_dump(),
            user_id=request.user_id,
            product_id=request.product_id,
        )
        await self.session.commit()
        return review


    async def update_review(
            self,
            review: ProductReview,
            request: ProductReviewUpdate
    ) -> None:
        await self.review_repo.update_review(
            review,
            **request.model_dump(),
        )
        await self.session.commit()


    async def delete_review(
            self,
            review_id: int
    ) -> None:
        await self.review_repo.delete_review(review_id)
        await self.session.commit()


    async def get_all_reviews(self):
        pass