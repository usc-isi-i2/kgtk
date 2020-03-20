import sys


class KGTKException(BaseException):
    return_code = 1

    def __init__(self):
        pass


class KGTKIntegerException(KGTKException):
    return_code = 2

    def __init__(self):
        pass


class KGTKExceptionHandler(object):
    def __call__(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            type, exc_val, exc_tb = sys.exc_info()
            return self.handle_exception(e, type, exc_val, exc_tb)

    def handle_exception(self, e, type, exc_val, exc_tb):
        if isinstance(e, KGTKException):
            return e.return_code
        return KGTKException.return_code


def kgtk_exception_handler(func, *args, **kwargs):
    exception_handler = KGTKExceptionHandler()
    return_code = exception_handler(func, *args, **kwargs)
    return return_code
