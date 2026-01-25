from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import manager
from app.auth.dependencies import get_auth_manager
from app.auth.manager import AuthManager
from app.auth.models import User
from app.auth.schemas import Token, UserRead, UserRegister, ChangePasswordSchema
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
    )->Token:
        """
        Авторизация поль. по логину и паролю
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
        """
        Метод нового поль.
        """
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
        return AuthManager(session)



    @router.get(
        "/me",
        summary="Получить текущего пользователя",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def get_me(
            self,
            session: AsyncSession = Depends(get_db),
    )->User:
        """
        Получение данных текущего поль.
        """
        return User

    @router.post(
        "/change_password",
        summary="Смена пароля",
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def change_password(
            self,
            request: ChangePasswordSchema,
            session: AsyncSession = Depends(get_db),
    ):
        """
        Смена пароля авторизованного поль.
        """
        response = await self.manager.change_password(User, request)
        return response


    @router.post(
        "/refresh_token",
        summary="Обновление токенов",
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def refresh_token(
            self,
            request: Token,
            session: AsyncSession = Depends(get_db),
    ):
        """
        Обновление JWT токенов
        """
        response = await self.manager.refresh_token(request)
        return response

