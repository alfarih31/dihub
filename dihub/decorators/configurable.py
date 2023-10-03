from copy import deepcopy
from typing import Callable, Type

from dihub.__internal.helpers import AnnotationOf, get_class_name
from dihub.constants import _MODULE_ANNOTATIONS
from dihub.types import Value, ModuleAnnotation, Configurable, Config

from .provider import provider


def configurable(config_type: Type[Config]) -> Callable[[Value], Configurable[Config, Value]]:
    def wrapper(decorated_class: Value) -> Configurable[Config, Value]:
        class Wrapper(decorated_class):
            def __init__(self, *args, **kwargs):
                super(decorated_class, self).__init__(*args, **kwargs)

            def __eq__(self, other):
                return super().__eq__(other)

            @classmethod
            def configure(cls, config: Config) -> Value:
                if not isinstance(config, config_type):
                    raise TypeError("Config not an instance of '%s'" % get_class_name(config_type))

                @provider(token=get_class_name(config_type))
                def config_wrapper() -> Config:
                    return config

                class Caller:
                    def __call__(self, *args, **kwargs):
                        return decorated_class(*args, **kwargs)

                Caller.__annotations__ = deepcopy(cls.__annotations__)

                module_annotation = AnnotationOf(Caller).get(_MODULE_ANNOTATIONS, ModuleAnnotation)
                module_annotation.providers.append(config_wrapper)

                return Caller()

        Wrapper.__annotations__.update(deepcopy(decorated_class.__annotations__))
        return Wrapper

    return wrapper
