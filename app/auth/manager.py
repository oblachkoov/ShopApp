from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import InvalidUsernamePassword, UsernameAlreadyConflict, EmailAlreadyExists, InvalidToken
from app.auth.models import User
from app.auth.repositore import UserRepository
from app.auth.schemas import RoleEnum, UserRead, ChangePasswordSchema, Token, UserRegister
from app.auth.services import PasswordServices, TokenServices


class AuthManager:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
        self.user_repo = UserRepository(session)
        self.password_service = PasswordServices()
        self.token_service = TokenServices()

    async def login(
            self,
            username: str,
            password: str
    ) -> Token:
        """
        Метод для входа в учётную запись

        проверяет наличие указанного username в базе данных

        проверяет правильность указанного пароля

        :param username: Имя поль.
        :param password: Пароль

        :param Unauthorized: Ошибка авторизауии

        :return: JWT Токен
        """
        user = await self.user_repo.get_user_by_username(username)
        if not user:
            raise InvalidUsernamePassword(
                "Invalid username or password. Please try again."
            )
        if not self.password_service.verify(password, user.hashed_password):
            raise InvalidUsernamePassword("Invalid username or password. Please try again.")

        access_token = self.token_service.encode(str(user.id))
        refresh_token = self.token_service.encode(str(user.id), True)
        return Token(access_token=access_token, refresh_token=refresh_token)


    async def register(
            self,
            request: UserRegister,
    ) -> User:
        """
        Метод для регистрации поль.

        Проверяем наличие username в БД

        Проверяет наличие почты

        Хэширует пароль

        Создаёт польз. в БД

        :param request: объект Pydantic модельки UserRegister
        :return:  Моделька созданного пользователя
        """
        user = await self.user_repo.get_user_by_username(request.username)

        if user:
            raise UsernameAlreadyConflict(
                "Username is already registered. Please try again."
            )
        user = await self.user_repo.get_user_by_email(request.email)
        if user:
            raise EmailAlreadyExists(
                "Email is already registered. Please try again."
            )

        hashed_password = self.password_service.hash(request.password)

        # user = await self.user_repo.create(
        #     username=request.username,
        #     email=request.email,
        #     hashed_password=hashed_password,
        #     fullname=request.fullname
        # )
        user = await self.user_repo.create(
            hashed_password=hashed_password,
            **request.model_dump(
                exclude={"password"}
            )
        )
        await  self.session.commit()
        return user

    async def get_me(
            self,
            token: str,
    ) -> User:
        """
        Метод для получения информации поль.

        Проверяет токен на валидность

        Достаём информацию по ИД из БД

        :param token: JWT Token
        :return: Моделька поль.
        """
        payload = self.token_service.decode(token)

        if payload.get("is_refresh", True):
            raise InvalidToken(
                "Invalid Credentials",
            )

        if not payload.get("sub") or not payload.get("sub").isdigit():
            raise InvalidToken(
                "Invalid Token"
            )

        user = await self.user_repo.get_user_by_id(int(payload.get("sub")))

        if not user:
            raise InvalidToken(
                "Invalid Credentials",
            )
        return user


    async def change_password(
            self,
            user: User,
            request: ChangePasswordSchema
    ) -> None:
        """
        Метод изменения пароля

        Проверяет старый пароль поль.

        Хэширует новый пароль и потом уже изменяет в БД

        Изменяет пароль в БД

        :param user: Моделька Пользователя
        :param request: моделька Pydantic ChangePasswordSchema
        :return: Ничего
        """
        if not self.password_service.verify(request.old_password, user.hashed_password):
            raise InvalidUsernamePassword("Invalid username or password. Please try again.")

        hashed_password = self.password_service.hash(request.new_password)

        await self.user_repo.update_password(
            user.id,
            hashed_password
        )

        await self.session.commit()



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
        payload = self.token_service.decode(token)

        if not payload.get("is_refresh"):
            raise InvalidToken(
                "Invalid Token",
            )
        if not payload.get("sub") or payload.get("sub").isdigit():
            raise InvalidToken(
                "Invalid Token",
            )

        access_token = self.token_service.encode(payload.get("sub"))
        refresh_token = self.token_service.encode(payload.get("sub"))
        return Token(access_token=access_token, refresh_token=refresh_token)



