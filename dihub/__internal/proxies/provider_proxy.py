from copy import deepcopy
from inspect import getmembers, isclass
from typing import Any, Type

from dihub.__internal.helpers import get_class_name
from dihub.types import Value, IProviderProxy, IProviderRunner


class ProviderProxy(IProviderProxy):
    __provide: Value
    __AFTER_START_CALLED = False

    @staticmethod
    def __release(provide: Value) -> Value:
        if isinstance(provide, IProviderProxy):
            return ProviderProxy.__release(provide.release())

        return provide

    def __init__(self, provide: Value):
        self.__provide = ProviderProxy.__release(provide)

    def __str__(self):
        if isinstance(self.__provide, type):
            return "<%s %s>" % (ProviderProxy.__name__, get_class_name(self.__provide))
        return "<%s %s object at %s>" % (ProviderProxy.__name__, get_class_name(self.__provide), hex(id(self.__provide)))

    def __eq__(self, other: Any):
        if isinstance(other, ProviderProxy):
            return self.__provide == other.__provide

        return False

    def deep_eq(self, other: Any) -> bool:
        if not self.__eq__(other):
            return False

        return id(self.__provide) == id(other.__provide)

    def on_boot(self):
        if isclass(self.__provide):
            for _, method in getmembers(self.__provide, predicate=lambda x: isinstance(x, ProviderProxy)):
                method.on_boot()
            self.__provide = self.__provide()

    def on_post_boot(self):
        if not isclass(self.__provide):
            for _, method in getmembers(self.__provide, predicate=lambda x: isinstance(x, ProviderProxy)):
                method.on_post_boot()

            if not self.__AFTER_START_CALLED and isinstance(self.__provide, IProviderRunner):
                self.__provide.after_started()
                self.__AFTER_START_CALLED = True

    def cast(self, metaclass: Type[Value]) -> Value:
        if isinstance(self.__provide, metaclass):
            return self
        raise TypeError("Can't cast, the provider %s doesn't implement '%s'" % (self.__provide, metaclass.__name__))

    def release(self) -> Value:
        return self.__provide

    def __getattr__(self, item):
        if item == "_ProviderProxy__provide":
            raise AttributeError()

        try:
            return getattr(self.__provide, item)
        except AttributeError:
            return self.release()

    def __copy__(self):
        return ProviderProxy(deepcopy(self.__provide))

    @property
    def provide(self) -> Value:
        return self.__provide
