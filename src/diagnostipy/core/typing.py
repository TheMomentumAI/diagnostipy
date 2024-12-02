from enum import Enum
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Enum)
FunctionMap = dict[T, Callable[..., Any]]
