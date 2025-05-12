import inspect


class CustomException(Exception):
    def __init__(self, message: str):
        frame = inspect.currentframe().f_back
        # Получаем self (если есть) для определения класса
        self_obj = frame.f_locals.get('self', None)
        class_name = self_obj.__class__.__qualname__ if self_obj else None
        method_name = frame.f_code.co_name

        if class_name:
            error_msg = f"Class {class_name}: Method - {method_name} - {message}"
        else:
            error_msg = f"Function - {method_name} - {message}"

        super().__init__(error_msg)


class TokenException(CustomException):
    """Primary exception for errors thrown in the get token post request."""
    pass


class SetSession(CustomException):
    """Base exception for errors caused within a get couriers."""
    pass
