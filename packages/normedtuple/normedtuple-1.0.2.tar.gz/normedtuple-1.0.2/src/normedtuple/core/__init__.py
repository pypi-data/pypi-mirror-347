import inspect
from typing import *

__all__ = ["normedtuple"]


def normedtuple(norm: Callable) -> type:
    "This decorator turns a norm function into a normed tuple class."

    class Ans(tuple):
        "This class will be returned. Before that the current doc string will be overwritten."

        def __new__(cls: type, /, *args: Any, **kwargs: Any) -> Any:
            "This magic method returns a new instance of the class."
            data = norm(cls, *args, **kwargs)
            obj = tuple.__new__(cls, data)
            return obj

    Ans.__doc__ = norm.__doc__
    Ans.__module__ = norm.__module__
    Ans.__name__ = norm.__name__
    oldsig = inspect.signature(norm)
    params = oldsig.parameters.values()
    newsig = inspect.Signature(parameters=params, return_annotation=Self)
    Ans.__new__.__signature__ = newsig
    Ans.__qualname__ = norm.__qualname__
    return Ans
