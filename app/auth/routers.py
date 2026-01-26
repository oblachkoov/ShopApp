from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from starlette import status


from app.auth.dependencies import get_auth_manager, get_current_user
from app.auth.manager import AuthManager
from app.auth.models import User
from app.auth.schemas import Token, UserRead, UserRegister, ChangePasswordSchema, RefreshToken

#TODO: "OAuth2PasswordRequestForm -> ОН У НАС multipart-data


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@cbv(router)
class AuthRouter:
    manager: AuthManager = Depends(get_auth_manager)

    @router.post(
        "/login",
        summary="Авторизация в систему", #Название нашего Эндпоинта
        response_model=Token,
        status_code=status.HTTP_201_CREATED, #Какой стату код он нам вернёт
        # responses={
        #
        # }#Какие ещё ответы он может вернуть
    )

    async def login(
            self,
            form_data: OAuth2PasswordRequestForm = Depends(),
    ):
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





    @router.get(
        "/me",
        summary="Получить текущего пользователя",
        response_model=UserRead,
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def get_me(
            self,
            user: User = Depends(get_current_user),
    ):
        """
        Получение данных текущего поль.
        """
        return user


    @router.post(
        "/change_password",
        summary="Смена пароля",
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def change_password(
            self,
            request: ChangePasswordSchema,
            user: User = Depends(get_current_user),
    ):
        """
        Смена пароля авторизованного поль.
        """
        response = await self.manager.change_password(user, request)
        return response


    @router.post(
        "/refresh_token",
        summary="Обновление токенов",
        status_code=status.HTTP_200_OK,
        responses={},
    )
    async def refresh_token(
            self,
            request: RefreshToken,
    ):
        """
        Обновление JWT токенов
        """
        response = await self.manager.refresh_token(request.refresh_token)
        return response

