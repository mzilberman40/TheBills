# import datetime
import time
import functools

DEBUG = 9   # Detailing level from 0 to 10)


def tracer(DEBUG=9):
    """
    DEBUG = 0 - will print nothing
    DEBUG >= 8 - will print func output
    DEBUG >= 9 - will print number of calls
    """
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if DEBUG > 0:
                print()
                try:
                    class_name = args[0].__class__.__name__ if args else "UnknownClass"
                except AttributeError:
                    class_name = None

                if class_name:
                    print(f"Class: {class_name}")

                print(f"Function: {func.__name__}: ")
                print(f"args: {args[1:]}, kwargs: {kwargs}")
                print()
            result = func(*args, **kwargs)
            if DEBUG > 0:
                print(f"Exiting {func.__name__}... ")
            if DEBUG > 7:
                print(f"Returned: {repr(result)}")
            print()
            if DEBUG > 8:
                wrapper.num += 1
                print(f'Was called: {wrapper.num}')
            print()
            return result
        wrapper.num = 0
        return wrapper
    return outer


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Executing time of {func.__name__}: {round(end_time - start_time, 4)} sec")
        return result
    return wrapper
