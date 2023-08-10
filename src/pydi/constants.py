from enum import Enum

_MODULE_ANNOTATIONS = "__PYDI_MODULE"
_PROVIDER_ANNOTATIONS = "__PYDI_PROVIDER"


class ProviderScope(Enum):
    GLOBAL = 1
    MODULE = 2
    LOCAL = 3
