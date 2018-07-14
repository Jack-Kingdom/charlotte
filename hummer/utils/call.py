import functools


def call_increase(value):
    """
    decrease value when func called.
    :param value: integer
    :return: decorator
    """

    value += 1

    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


def call_decrease(value):
    """
    decrease value when func called.
    :param value: integer
    :return: decorator
    """

    value -= 1

    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper
