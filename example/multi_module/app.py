from A import AModule
from B import BModule, BService, IBService
from pydi.decorators import module, root, for_root


@root
@module(imports=[for_root(AModule), BModule])
class App: ...


if __name__ == "__main__":
    root_app = App()

    # Get B module ref
    B_MODULE_REF = root_app[BModule]

    # Get the B Service from B Module
    b_service = B_MODULE_REF.providers[BService][0].cast(IBService)

    b_service.print_all()
