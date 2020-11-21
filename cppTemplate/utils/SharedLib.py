import importlib
import multiprocessing as mp
from functools import partial

class SharedLib:
    """
    Wrapper for compiled C++ libraries allowing hot-reloading by calling library code in a new process.
    
    The new process will import the library from disk rather than use the stale version in memory. 
    This side-steps the inability of Python to reload pybind modules.

    Args:
        lib: name of the shared library to be wrapped
    """
    def __init__(self, lib: str):
        self.lib = lib

    def __getattr__(self, func):
        return partial(call, self.lib, func)


def call(lib, func, *args):
    """Call a library function in a new process and return the result
    Approximately equivalent to
        from lib import func
        func(*args)

    Args:
        lib: library defining the target function
        func: target function to call
        *args: arguments passed to the function
    Returns:
        forwarded return value of function invocation
    """

    def fn(q):
        _lib = importlib.import_module(lib, '.')
        q.put(getattr(_lib, func)(*args))
    q = mp.Queue()
    p = mp.Process(target=fn, args=(q,))
    p.start()
    ret = q.get()
    p.join()
    return ret
