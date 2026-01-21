import re
from datetime import datetime
from enum import Enum


from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

from app.auth.validators import validate_password


class UserBase(BaseModel):
    """
    Базовая Pydantic Моделька Поль.

    Attributes:
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.
    """
    username: str = Field(min_length=3, max_length=320)
    email: EmailStr
    full_name: str = Field(max_length=3, min_length=512)

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value: str) -> str:
        """
        Функция для валидации Имени Поль.

        Проверка на то что Имя польз. Начинается с буквы
        Проверка на то что Имя поль. Может содержать только буквы цифры и _

        :param value:  Значение имени поль.
        :return: Валидированное имя поль.
        """

        #Проверка

        #Первое - Первая буква не цифра или спец. Символ

        #Второе - нельзя исполь. Другие спец. Символы

        if re.fullmatch(
                r'^[A-Za-z][A-Za-z0-9_]*$',
            value,
        ):
            raise ValueError("Username cannot contain special characters and _")
        return value.lower()



class UserRegister(UserBase):
    """
    Pydantic Моделька для регистрации пользователя

        Attributes:
        password: Пароль
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.

    """
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        """
        Метод валидации пароля

        Пароль должен состоять из строчных и заглавных букв, цифр, и спец. Символов
        :param value:  значение пароля
        :return: значение пароль
        """
        return validate_password(value)


class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    moderator = "moderator"

class UserCreate(BaseModel):
    """
    Pydantic Моделька для создания поль.

    Attributes:
        role: Роль Польз.
        password: Пароль
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.
    """
    role: RoleEnum


class UserUpdate(UserBase):
    """
    Pydantic Моделька для обновления поль.

    Attributes:
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.
    """
    pass



class UserUpdateAdmin(UserBase):
    """
    Pydantic Моделька для обновления  поль. админом

    Attributes:
        role: Роль Польз.
        is_active: Флажок активности
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.
    """
    role: RoleEnum
    is_active: bool


class ChangePasswordSchema(BaseModel):
    """
        Pydantic Моделька для изменения пароля
    """

    old_password: str
    new_password: str

    @field_validator("new_password", mode="before")
    @classmethod
    def validate_password(cls, value):
        """
        Метод валидации пароля
        """
        return validate_password(value)

    @model_validator
    def cjeck_password_match(self):
        if self.old_password != self.new_password:
            raise ValueError("Passwords don't match")
        return self



class UserRead(UserBase):
    """
    Pydantic моделька для просмотра поль.

    Attributes:
        id: уникальный идентификатор поль.
        role: Роль Польз.
        is_active: Флажок активности
        username (str): - Имя Поль.
        email: Почта поль.
        fullname: Полное имя поль.
        created_at: Временная отметка создания поль.
        updated_at: Временная отметка обновления поль.
    """
    id: int
    role: RoleEnum
    created_at: datetime
    updated_at: datetime | None = None


