import warnings


def deprecated(msg=''):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn("{}: this function is deprecated. {}".format(func.__name__, msg))
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator
