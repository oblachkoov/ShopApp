from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class IntIdMixin:
    """
    IntIdMixin: Класс Миксин для добавления поля ИД в виде Целых Чисел
    """
    id = Column(BigInteger, primary_key=True, autoincrement=True)


class TimeActionMixin:
    """
    TimeActionMixin: Класс Миксин для добавления Полей с временной отметкой о создании и обновления
    """
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



