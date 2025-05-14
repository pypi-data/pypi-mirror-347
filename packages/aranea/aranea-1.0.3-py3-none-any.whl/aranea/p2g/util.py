"""
Utilities for P2G.
"""

import inspect
import logging
import typing
from inspect import Parameter
from typing import Annotated, Any, Callable, ParamSpec, TypeVar

from typing_extensions import Doc

_logger = logging.getLogger(__file__)

R = TypeVar("R")
P = ParamSpec("P")


REM = Annotated[float, "The Root Element Size"]
DictTextBlock = dict[str, Any]


def __type2str(t: TypeVar) -> str:
    if typing.get_args(t):
        return str(t)
    if hasattr(t, "__name__"):
        return t.__name__
    return str(t)


def __func2param_docstring(
    func: Callable[P, R], *, keyword_only: bool = False, no_kwargs: bool = True
) -> str:
    _docstring = ""
    params = inspect.signature(func).parameters

    if keyword_only:
        # restrict params to keyword parameters
        params = {  # type: ignore
            name: param
            for name, param in params.items()
            if param.kind == inspect.Parameter.KEYWORD_ONLY
        }

    if no_kwargs:
        # remove kwargs from params
        params = {  # type: ignore
            name: param
            for name, param in params.items()
            if not param.kind == inspect.Parameter.VAR_KEYWORD
        }

    # generate sphinx docstrings for each parameter
    for name, param in params.items():
        defaults_to = ""
        if param.default is not Parameter.empty:
            defaults_to = f", defaults to {param.default}"
        if typing.get_origin(param.annotation) is Annotated:
            param_type, param_doc = typing.get_args(param.annotation)
            if isinstance(param_doc, str):
                _docstring += f":param {name}: {param_doc}{defaults_to}\n"
            elif isinstance(param_doc, Doc):
                _docstring += f":param {name}: {param_doc.documentation}{defaults_to}\n"
            _docstring += f":type {name}: {__type2str(param_type)}\n"
        elif param.annotation is not Parameter.empty:
            # NOTE: we use the param type as documentation when not documentation provided
            if param.kind == inspect.Parameter.KEYWORD_ONLY:
                _logger.warning(
                    "Missing parameter type annotation for %s of %s", name, func.__name__
                )
            _docstring += f":param {name}: {__type2str(param.annotation)}{defaults_to}\n"
            _docstring += f":type {name}: {__type2str(param.annotation)}\n"
    return _docstring


def __func2return_docstring(func: Callable[P, R]) -> str:
    if func.__annotations__.get("return") is None:
        return ":rtype: None"

    _docstring = ""
    ret_annot = typing.get_type_hints(func, include_extras=True).get("return")
    if ret_annot is None:
        return ""

    if typing.get_origin(ret_annot) is Annotated:
        ret_type, ret_doc = typing.get_args(ret_annot)
        if isinstance(ret_doc, str):
            _docstring += f":return: {ret_doc}\n"
        elif isinstance(ret_doc, Doc):
            _docstring += f":return: {ret_doc.documentation}\n"
        _docstring += f":rtype: {__type2str(ret_type)}\n"
    elif ret_annot is not Parameter.empty:
        # NOTE: we use the type as default param documentation
        _logger.warning("Missing return type annotation for %s", func.__name__)
        _docstring += f":return: {__type2str(ret_annot)}\n"
        _docstring += f":rtype: {__type2str(ret_annot)}"

    return _docstring


def gendocstring(real_function: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator for generating sphinx docstrings.
    """
    new_function = real_function

    _docstring = real_function.__doc__ or ""
    _docstring += "\n"
    _docstring += __func2param_docstring(real_function)
    _docstring += __func2return_docstring(real_function)
    new_function.__doc__ = _docstring
    return new_function


def take_annotation_from(*funcs: Callable[..., Any]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator factory to append keyword parameter type annotations from other functions
    to the function's docstring.
    """

    def __decorator(real_function: Callable[P, R]) -> Callable[P, R]:
        new_function = real_function

        _docstring = real_function.__doc__ or ""
        _docstring += "\n"
        _docstring += "Calls functions: "
        _docstring += ", ".join([f"`{f.__name__}`" for f in funcs])
        _docstring += "\n"

        _func_params = ""
        _func_params += __func2param_docstring(real_function)
        for func in funcs:
            _func_params += __func2param_docstring(func, keyword_only=True)
            if new_function.__kwdefaults__ is None:  # pyright: ignore
                new_function.__kwdefaults__ = {}
            new_function.__kwdefaults__.update(func.__kwdefaults__ or {})

        _func_params += __func2return_docstring(real_function)

        _docstring += "\n"
        _docstring += _func_params
        new_function.__doc__ = _docstring
        return new_function

    return __decorator


@gendocstring
def color2str(
    color: tuple[float, float, float] | None,
) -> Annotated[str, "The color as hex string"]:
    """
    Convert color as float triple to hex string.
    """

    if color is None:
        return "#000000"
    return "#" + "".join([f"{int(x * 255):02x}" for x in color])


@gendocstring
def is_horizontal(
    x0: float, y0: float, x1: float, y1: float
) -> Annotated[bool, "Whether the geometry is horizontal"]:
    """
    Check if the rectangle is horizontal
    """

    return abs(x1 - x0) > abs(y1 - y0)
