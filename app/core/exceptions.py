class Unauthorized(Exception):
    """
    Вызывается когда у поль. Ошибка связана с аутентификацией
    """


class Forbidden(Exception):
    """
    Вызывается когда у поль. Ошибка связана с правами
    """


class NotFound(Exception):
    """
    Вызывается когда не был найден объект
    """


class Conflict(Exception):
    """
    Вызывается когда происходит конфликт
    """


class BadRequest(Exception):
    """
    Вызывается когда запрос был неправильным
    """

