from abc import ABC, abstractmethod

from pydi.constants import ProviderScope
from pydi.decorators import provider, export

GlobalScopedAService = "GlobalScopedAService"
ModuleScopedAService = "ModuleScopedAService"
LocalScopedAService = "LocalScopedAService"


class IAService(ABC):
    @abstractmethod
    def print(self): ...


@export
@provider(token=GlobalScopedAService)
class __GlobalScopedAService(IAService):
    def print(self):
        print(self.__str__())


@export
@provider(token=ModuleScopedAService, scope=ProviderScope.MODULE)
class __ModuleScopedAService(__GlobalScopedAService): ...


@export
@provider(token=LocalScopedAService, scope=ProviderScope.LOCAL)
class __LocalScopedAService(__GlobalScopedAService): ...
