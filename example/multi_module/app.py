from A import AModule
from B import BModule, BService, IBService
from dihub.decorators import module, root, for_root
from dihub.types import IRootRunner, IModuleDelegate


@root
@module(imports=[for_root(AModule), BModule])
class App(IRootRunner):
    __root_ref: IModuleDelegate

    @property
    def root_ref(self) -> IModuleDelegate:
        return self.__root_ref

    def after_started(self, root_module_delegate: IModuleDelegate):
        self.__root_ref = root_module_delegate


if __name__ == "__main__":
    root_app = App()

    # Get B module ref
    B_MODULE_REF = root_app.root_ref[BModule]

    # Get the B Service from B Module
    b_service = B_MODULE_REF.providers[BService][0].cast(IBService)

    b_service.print_all()
