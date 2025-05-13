"Utility functions with dsloader"

import time


def time_spent(func):
    """
    Decorator to print the time spent executing a function.

    Parameters
    ----------
    func : Callable
        The function whose execution time is to be measured.

    Returns
    -------
    Callable
        A wrapped function that prints the execution time.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nTime spent: {elapsed_time:.2f} seconds")
        return result

    return wrapper
