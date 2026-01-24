from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import manager
from app.auth.dependencies import get_auth_manager
from app.auth.manager import AuthManager
from app.auth.schemas import Token, UserRead, UserRegister
from app.core.dependencies import get_db

#TODO: "OAuth2PasswordRequestForm -> ОН У НАС multipart-data


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@cbv(router)
class AuthRouter:
    manager: AuthManager = Depends(get_auth_manager),

    @router.post(
        "/login",
        summary="Авторизация в систему", #Название нашего Эндпоинта
        response_model=Token,
        status_code=status.HTTP_200_CREATED, #Какой стату код он нам вернёт
        responses={

        }#Какие ещё ответы он может вернуть
    )
    async def login(
            self,
            form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        """

        """
        response = await self.manager.login(
            username=form_data.username,
            password=form_data.password,
        )
        return response


    @router.post(
        "/register",
        summary="Регистрация Пользователя",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        responses={

        }
    )
    async def register(
            self,
            request: UserRegister,
    ):
        response = await self.manager.register(request)
        return response

    


    async def get_auth_manager(
            session: AsyncSession = Depends(get_db),
    ):
        """
        Функция для создания объект AuthManager
        :param session:
        :return:
        """