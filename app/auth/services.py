import token
from datetime import datetime, timedelta


from jose import jwt, JWTError
from passlib.hash import argon2

from app.auth.exceptions import InvalidToken
from app.core.settings import settings




class PasswordServices:
    """
    Класс для работы с паролями
    """
    def hash(self, password: str) -> str:
        """
        Метод будет шифрировать указанный пароль

        :param password: пароль
        :return: зашифрированный пароль
        """
        return argon2.hash(
            password
        )


    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Метод для поверки введённого  пароля с зашифрованным

        :param password: Введённый пароль
        :param password_db: Зашифрованный пароль
        :return: True если пароль совпал False ли нет
        """
        return argon2.verify(
            password,
            hashed_password
        )



class TokenServices:
    """
    Класс для работы с токеном
    """
    def encode(self, sub: str, is_refresh: bool = False):
        """
        Метод для создания JWT токена

        :param sub: Субъект для которого мы создаём токен(поль.)
        :param is_refresh: Флажок обозначающий создания refresh токена либо access токена
        :return: JWT токена
        """

        exp = timedelta(minutes=settings.REFRESH_EXPIRES) if is_refresh else timedelta(minutes=settings.ACCESS_EXPIRES)
        payload = {
            "sub": sub,
            "is_refresh": is_refresh,
            "exp": datetime.now() + exp
        }
        return jwt.encode(
            payload,
            algorithm=settings.TOKEN_ALGORITHM,
            key=settings.TOKEN_SECRET_KEY,
        )


    def decode(self, token: str) -> dict:
        """
        Метод для рафщиврования JWT токена
        :param token: JWT токен
        :return: Payload то есть информацию о нашем субъекте
        """
        try:
            payload = jwt.decode(
                token,
                algorithms=[settings.TOKEN_ALGORITHM],
                key=settings.TOKEN_SECRET_KEY,
            )
        except JWTError:
            raise InvalidToken(
                "Invalid token",
            )
        return payload