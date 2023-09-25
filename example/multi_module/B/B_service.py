from abc import ABC, abstractmethod

from A import GlobalScopedAService, ModuleScopedAService, LocalScopedAService, IAService

from dihub.decorators import provider, export, inject

BService = "BService"


class IBService(ABC):
    @abstractmethod
    def print(self): ...

    def print_all(self): ...


@export
@provider(token=BService)
class __BService(IBService):
    global_a_service: IAService = inject(GlobalScopedAService)
    module_a_service: IAService = inject(ModuleScopedAService)
    local_a_service: IAService = inject(LocalScopedAService)

    def print(self):
        print(self.__str__())

    def print_all(self):
        self.print()
        self.global_a_service.print()
        self.module_a_service.print()
        self.local_a_service.print()
