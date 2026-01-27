from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from app.auth.dependencies import is_admin, get_current_user
from app.auth.models import User
from category.dependencies import get_category_manager
from category.manager import CategoryManager
from category.schemas import CategoryCreate, CategoryUpdate, CategoryDelete

router = APIRouter(
    prefix="/categories",
    tags=["category"]
)


@cbv(router)
class AuthRouter:
    manager: CategoryManager = Depends(get_category_manager)


    @router.post(
        "/",
        summary="создание категории",
        status_code=status.HTTP_200_OK,
    )
    async def create(
            self,
            request: CategoryCreate,
            user: User = Depends(get_current_user)
    ):
        """
        Метод для создания категории
        """
        response = await self.manager.create_category(request)
        return response


    @router.get(
        "/{category_id}",
        summary="получение категории по ид",
        status_code=status.HTTP_200_OK,
    )
    async def get_by_id(
            self,
            category_id: int,
    ):
        """
        Метод для получения категории по ид
        """
        response = await self.manager.get_category(category_id)
        return response


    @router.get(
        "/",
        summary="получение категорий",
        status_code=status.HTTP_200_OK,
    )
    async def get_all(
            self,
    ):
        """
        Метод для получения всех категорий
        """
        response = await self.manager.get_all_categories()
        return response


    @router.put(
        "/",
        summary="обновление категории",
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def update(
            self,
            request: CategoryUpdate
    ):
        """
        Метод для обновления категории
        """
        response = await self.manager.update_category(request)
        return response


    @router.delete(
        "/",
        summary="удаление категории",
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def delete(
            self,
            request: CategoryDelete
    ):
        """
        Метод для удаления категории
        """
        response = await self.manager.delete_category(request)
        return response