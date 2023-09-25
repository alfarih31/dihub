from app_controller import AppController
from fastapi_module import FastAPIModule, FastAPIProvider
from dihub.decorators import root, module
from dihub.plugins import ASGI


@root(plugins=[ASGI(from_module=FastAPIModule, from_provider=FastAPIProvider)])
@module(imports=[FastAPIModule], providers=[AppController])
class App:
    """
    Run with ASGI server. Example of using uvcorn:
    uvcorn app:App
    """
    pass
