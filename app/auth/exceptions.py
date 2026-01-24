from app.core.exceptions import Unauthorized, Conflict


class InvalidUsernamePassword(Unauthorized):
    """
    Ошибка username или password
    """


class InvalidToken(Unauthorized):
    """
    Ошибка Невалидного Токена
    """

class UsernameAlreadyConflict(Conflict):
    """
    Ошибка! имя уже занята
    """

class EmailAlreadyExists(Conflict):
    """
    Ошибка! почта уже занята
    """