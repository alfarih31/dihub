from fastapi_module import FastAPIProvider
from dihub.decorators import inject
from dihub.decorators import provider
from dihub.types import IProviderRunner


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
