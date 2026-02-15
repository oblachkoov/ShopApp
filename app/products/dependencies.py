from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.dependencies import get_db
from app.core.exceptions import Forbidden
from app.products.managers.characteristic_manager import CharacteristicManager
from app.products.managers.product_manager import ProductManager
from app.products.managers.review_manager import ReviewManager
from app.products.models import Product, ProductReview


async def get_product_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта ProductManager

    :param session: сессия бд

    :return: объект ProductManager
    """

    return ProductManager(session)



async def get_product_or_404(
    product_id: int,
    manager: ProductManager = Depends(get_product_manager),
):
    """
    Функция для поиска продукта
    Если продукта нет вызывает ошибку 404

    :param product_id: ИД продукта
    :param manager: объект ProductManager

    :return: моделька продукта
    """

    return await manager.get_product(product_id)




async def get_characteristics_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта ProductCharacteristicsManager

    :param session: сессия бд

    :return: объект ProductCharacteristicsManager
    """

    return CharacteristicManager(session)


async def get_characteristics_or_404(
    characteristic_id: int,
    product: Product = Depends(get_product_or_404),
    manager: CharacteristicManager = Depends(get_characteristics_manager),
):
    """
    Функция для поиска характеристики продукта
    Если характеристики нет вызывает ошибку 404

    :param characteristic_id: ИД характеристики
    :param product: объект продукта
    :param manager: объект ProductCharacteristicsManager

    :return: моделька характеристики
    """


    return await manager.get_characteristic(product, characteristic_id)


async def get_review_or_404(
    review_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для поиска отзыва
    Если отзыва нет вызывает ошибку 404

    :param review_id: ИД отзыва
    :param session: сессия бд

    :return: моделька отзыва
    """

    manager = ReviewManager(session)
    return await manager.get_review(review_id)


async def is_review_owner(
        review: ProductReview,
        user: User = Depends(get_current_user)
) -> None:
    """
    Функция для проверки является ли пользователь автором отзыва

    :param review: моделька отзыва
    :param user: моделька пользователя

    :return: ничего
    """
    if user.id != review.user_id:
        raise Forbidden(
            "You don't have permission"
        )