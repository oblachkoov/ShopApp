from urllib.request import Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import RoleEnum, UserRead, ChangePasswordSchema


class AuthManager:
    def __init__(
            self,
            session: AsyncSession
    ):
        pass

    async def login(
            self,
            username: str,
            password: str
    ):
        """
        Метод для входа в учётную запись

        проверяет наличие указанного username в базе данных

        проверяет правильность указанного пароля

        :param username: Имя поль.
        :param password: Пароль

        :param Unauthorized: Ошибка авторизауии

        :return: JWT Токен
        """
        pass


    async def register(
            self,
            request: Request,
    ) -> UserRead:
        """
        Метод для регистрации поль.

        Проверяем наличие username в БД

        Проверяет наличие почты

        Хэширует пароль

        Создаёт польз. в БД

        :param request: объект Pydantic модельки UserRegister
        :return:  Моделька созданного пользователя
        """


    async def get_me(
            self,
            token: str,
    ) -> UserRead:
        """
        Метод для получения информации поль.

        Проверяет токен на валидность

        Достаём информацию по ИД из БД

        :param token: JWT Token
        :return: Моделька поль.
        """


    async def change_password(
            self,
            user_id: int,
            request: ChangePasswordSchema
    ) -> None:
        """
        Метод изменения пароля

        Проверяет наличие поль.

        Проверяет старый пароль поль.

        Хэширует новый пароль и потом уже изменяет в БД

        Изменяет пароль в БД

        :param user_id: ИД Пользователя
        :param request: моделька Pydantic ChangePasswordSchema
        :return: Ничего
        """


    async def refresh_token(
            self,
            token: str
    ):
        """
        Метод для обновление токенов

        Проверяет валидность токена который нам поль. дал

        Создаёт новую пару токенов

        :param token: JWT Token
        :return: JWT Token
        """


