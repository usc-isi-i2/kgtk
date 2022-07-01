import sys
import warnings
import traceback
import sh


class KGTKException(BaseException):
    return_code = 1
    message = 'KGTKException found\n'

    def __init__(self, message):
        self.message = message


def kgtk_exception_auto_handler(e: Exception):
    if isinstance(e, (sh.SignalException_SIGPIPE, BrokenPipeError)):
        return
    elif isinstance(e, KGTKException):
        raise e
    raise KGTKException(KGTKException.message + str(e))


class KGTKArgumentParseException(KGTKException):
    # same as https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.error
    return_code = 2


class KGTKDependencyException(KGTKException):
    return_code = 5


class KGTKSyntaxException(KGTKException):
    return_code = 900


class InvalidParameter(Exception):
    pass


class WrongFormatURIException(Exception):
    pass


class PrefixNotFoundException(Exception):
    pass


class PrefixAlreadyUsedException(Exception):
    pass


class SplitURIWithUnknownPrefix(Exception):
    pass


class InvalidGraphNodeValueError(Exception):
    pass


class UnknownLiteralType(Exception):
    pass


class KGTKExceptionHandler(object):
    def __init__(self, debug=False):
        self._debug = debug

    def __call__(self, func, *args, **kwargs):
        try:
            return_code = func(*args, **kwargs) or 0
            if return_code != 0:
                warnings.warn('Please raise exception instead of returning non-zero value')
            return return_code
        except (sh.SignalException_SIGPIPE, BrokenPipeError):
            pass
        except KeyboardInterrupt:
            raise
        except BaseException:
            type_, exc_val, exc_tb = sys.exc_info()
            return self.handle_exception(type_, exc_val, exc_tb)

    def handle_exception(self, type_, exc_val, exc_tb):
        if self._debug:
            traceback.print_exception(type_, exc_val, exc_tb)  # the output goes to sys.stderr

        if isinstance(exc_val, KGTKException):
            print("%s" % exc_val.message, file=sys.stderr)
            return exc_val.return_code

        warnings.warn('Please raise KGTKException instead of {}'.format(type_))
        print("%s" % KGTKException.message, file=sys.stderr)
        return KGTKException.return_code


def kgtk_exception_handler(func, *args, **kwargs):
    exception_handler = KGTKExceptionHandler()
    return_code = exception_handler(func, *args, **kwargs)
    return return_code
