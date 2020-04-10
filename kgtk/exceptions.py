import sys
import warnings


class KGTKException(BaseException):
    return_code = 1
    message = 'KGTKException found\n'

    def __init__(self, message):
        self.message = message


class KGTKArgumentParseException(KGTKException):
    # same as https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.error
    return_code = 2


# class KGTKExampleException(KGTKException):
#     return_code = 1000  # please allocate a value which is gte 1000


class KGTKExceptionHandler(object):
    def __call__(self, func, *args, **kwargs):
        try:
            return_code = func(*args, **kwargs) or 0
            if return_code != 0:
                warnings.warn('Please raise exception instead of returning non-zero value')
            return return_code
        except BrokenPipeError:
            pass
        except BaseException:
            type_, exc_val, exc_tb = sys.exc_info()
            return self.handle_exception(type_, exc_val, exc_tb)

    def handle_exception(self, type_, exc_val, exc_tb):
        if isinstance(exc_val, KGTKException):
            sys.stderr.write(exc_val.message)
            return exc_val.return_code

        warnings.warn('Please raise KGTKException instead of {}'.format(type_))
        sys.stderr.write(KGTKException.message)
        return KGTKException.return_code


def kgtk_exception_handler(func, *args, **kwargs):
    exception_handler = KGTKExceptionHandler()
    return_code = exception_handler(func, *args, **kwargs)
    return return_code
