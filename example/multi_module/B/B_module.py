from pydi.decorators import module

from .B_service import __BService


@module(imports=[], providers=[__BService])
class BModule: ...
