from typing import Callable, Awaitable

from pydi.types import IRootPlugin, IModuleDelegate, InjectToken


class ASGI(IRootPlugin):
    from_provider: InjectToken
    from_module: type = None
    asgi_provider: Callable[..., Awaitable[None]] = None

    def __init__(self, from_provider: InjectToken, from_module: type = None):
        self.from_module = from_module
        self.from_provider = from_provider

    async def __asgi_async_call__(self, *args, **kwargs):
        return await self.asgi_provider(*args, **kwargs)

    def __call__(self, root_module_delegate: IModuleDelegate):
        if self.from_module is not None:
            self.asgi_provider = root_module_delegate[self.from_module].providers[self.from_provider][0].release()
        else:
            self.asgi_provider = root_module_delegate.providers[self.from_provider][0].release()

        setattr(root_module_delegate, "__call__", self.__asgi_async_call__)
