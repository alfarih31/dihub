from dihub.decorators import module

from .A_service import __GlobalScopedAService, __ModuleScopedAService, __LocalScopedAService


@module(providers=[__GlobalScopedAService, __ModuleScopedAService, __LocalScopedAService])
class AModule: ...
