from copy import deepcopy
from inspect import getmembers, isclass
from typing import Any

from pydi.typing import Provide


class ProviderProxy:
    __provide: Provide
    __ACTUAL_INIT = "__ACTUAL_INIT"

    def __init__(self, provide: Provide):
        if isclass(provide):
            setattr(provide, self.__ACTUAL_INIT, provide.__init__)
            provide.__init__ = lambda *args: None

        self.__provide = provide

    # def __get__(self, *args, **kwargs):
    #     return self.__provide

    def __str__(self):
        return "<%s '%s'>" % (self.__repr__(), str(self.__provide))

    def __eq__(self, other: Any):
        if isinstance(other, ProviderProxy):
            return self.__provide == other.__provide
        elif isinstance(other, type):
            return self.__provide == other

        return False

    def on_boot(self):
        if isclass(self.__provide):
            for _, method in getmembers(self.__provide, predicate=lambda x: isinstance(x, ProviderProxy)):
                method.on_boot()
            self.__provide = self.__provide()

    def on_post_boot(self):
        if isinstance(self.__provide, type(self.__provide)):
            for _, method in getmembers(self.__provide, predicate=lambda x: hasattr(x, self.__ACTUAL_INIT) and not isclass(x)):
                mi = getattr(method, self.__ACTUAL_INIT)
                mi()

            if hasattr(self.__provide, self.__ACTUAL_INIT):
                getattr(self.__provide, self.__ACTUAL_INIT)()

    def __getattr__(self, item):
        return getattr(self.__provide, item)

    def __copy__(self):
        # Avoiding copied ProviderProxy.provide is a ProviderProxy
        if isinstance(self.__provide, ProviderProxy):
            return self.__provide.__copy__()

        return ProviderProxy(deepcopy(self.__provide))

    @property
    def provide(self) -> Provide:
        return self.__provide
