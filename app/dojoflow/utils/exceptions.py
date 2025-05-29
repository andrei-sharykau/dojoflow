"""
Кастомные исключения для DojoFlow
"""


class DojoFlowException(Exception):
    """
    Базовое исключение для DojoFlow
    """
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class PermissionException(DojoFlowException):
    """
    Исключение для ошибок прав доступа
    """
    def __init__(self, message: str = "У вас нет прав для выполнения этого действия"):
        super().__init__(message, 'permission_denied')


class ValidationException(DojoFlowException):
    """
    Исключение для ошибок валидации
    """
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, 'validation_error')


class ClubAccessException(PermissionException):
    """
    Исключение для ошибок доступа к клубу
    """
    def __init__(self, message: str = "У вас нет доступа к этому клубу"):
        super().__init__(message)


class StudentAccessException(PermissionException):
    """
    Исключение для ошибок доступа к студенту
    """
    def __init__(self, message: str = "У вас нет доступа к этому студенту"):
        super().__init__(message)


class AttestationValidationException(ValidationException):
    """
    Исключение для ошибок валидации аттестации
    """
    def __init__(self, message: str = "Ошибка валидации аттестации"):
        super().__init__(message) 