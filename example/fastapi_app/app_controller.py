from fastapi_module import FastAPIProvider
from pydi.decorators import inject
from pydi.decorators import provider
from pydi.types import IProviderRunner


@provider
class AppController(IProviderRunner):
    fast_api: FastAPIProvider = inject(FastAPIProvider)

    def after_started(self):
        self.fast_api.get("/")(self.index)
        self.fast_api.get("/home")(self.home)

    async def index(self):
        return "Index"

    async def home(self):
        return "Home"
