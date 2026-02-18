from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.products.dependencies import get_review_or_404
from app.products.managers.review_manager import ReviewManager
from app.products.models import ProductReview
from app.products.schemas import (
    ProductReviewCreate,
    ProductReviewUpdate,
)

router = APIRouter(
    prefix="/reviews",
    tags=["review"]
)


@cbv(router)
class ReviewRouter:
    manager: ReviewManager = Depends(get_review_or_404())

    @router.post("/{product_id}")
    async def create_review(
            self,
            product_id: int,
            request: ProductReviewCreate,
            user: User = Depends(get_current_user)
    ):
        review = await self.manager.create_review(
            product_id=product_id,
            user_id=user.id,
            request=request
        )
        return review


    @router.get("/{review_id}")
    async def get_review(
            self,
            review: ProductReview = Depends(get_review_or_404)
    ):
        return review

    @router.put("/{review_id}")
    async def update_review(
            self,
            request: ProductReviewUpdate,
            review: ProductReview = Depends(get_review_or_404),
            user: User = Depends(get_current_user)
    ):
        if review.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can update only your own review"
            )

        await self.manager.update_review(
            review_id=review.id,
            request=request
        )

    @router.delete("/{review_id}")
    async def delete_review(
            self,
            review: ProductReview = Depends(get_review_or_404),
            user: User = Depends(get_current_user)
    ):
        if review.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own review"
            )

        await self.manager.delete_review(review.id)
