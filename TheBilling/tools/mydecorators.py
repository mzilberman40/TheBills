import datetime
DEBUG = 9   # Detailing level from 0 to 10)


def tracer(DEBUG):
    """
    DEBUG = 0 - will print nothing
    DEBUG > 8 - will print func output
    """

    def outer(func):
        def wrapper(*args, **kwargs):
            if DEBUG > 0:
                print()
                print(f"Function: {func.__name__}: ")
                # print(f"Caller: {func.}")
                print(f"args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            if DEBUG > 0:
                print(f"Exiting {func.__name__}... ")
                if DEBUG > 8:
                    print(f"Returned: {result}")
                print()
            return result
        return wrapper
    return outer


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        print(f"Executing time: {datetime.datetime.now() - start_time}")
        return result
    return wrapper
