from typing import Any

from pydi.typing import _as_primitive


class PrimitiveProxy:
    __primitive_value: _as_primitive

    def __init__(self, primitive_value: _as_primitive):
        self.__primitive_value = primitive_value

    def __get__(self, *args, **kwargs) -> _as_primitive:
        return self.__primitive_value

    def __str__(self):
        return self.__primitive_value.__str__()

    def __eq__(self, other: Any):
        return self.__primitive_value.__eq__(other)

    def __repr__(self):
        return self.__primitive_value.__repr__()
