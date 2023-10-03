from typing import Any, Generic

from dihub.types import _as_primitive, Value


class PrimitiveProxy(Generic[Value]):
    __name: str
    __primitive_value: _as_primitive

    def __init__(self, name: str, primitive_value: _as_primitive):
        self.__primitive_value = primitive_value
        self.__name = name

    @property
    def __name__(self):
        return self.__name

    def __get__(self, *args, **kwargs) -> _as_primitive:
        return self.__primitive_value

    def __str__(self):
        return self.__primitive_value.__str__()

    def __eq__(self, other: Any):
        return self.__primitive_value.__eq__(other)

    def __repr__(self):
        return self.__primitive_value.__repr__()

    def set_actual_value(self, value: Value):
        self.__primitive_value = value
