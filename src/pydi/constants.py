from enum import Enum

_MODULE_ANNOTATIONS = "__PYDI_MODULE"
_PROVIDER_ANNOTATIONS = "__PYDI_PROVIDER"


class ProviderScope(Enum):
    GLOBAL = 1, 'Provider is only one SINGLE instance (singleton) which shared to all module imports'
    MODULE = 2, 'Provider is UNIQUE instance on each module imports'
    LOCAL = 3, 'Provider is UNIQUE instance on each providers'
