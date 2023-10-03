from inspect import iscoroutinefunction
from typing import Type

from dihub.__internal.delegates import ModuleDelegate
from dihub.__internal.helpers import validate_dihub_module
from dihub.types import Value, IRootRunner, Plugins


def __process_root_decorator(cls: Value, plugins: Plugins) -> Type[Value]:
    validate_dihub_module(cls)

    def __call__(*args, **kwargs):
        __module_delegate = ModuleDelegate(cls, None)
        __module_delegate.on_boot()
        __module_delegate.on_post_boot()

        # Apply plugins
        for p in plugins:
            p(__module_delegate)

        base_class_instance = __module_delegate.base_class(*args, **kwargs)

        if isinstance(base_class_instance, IRootRunner):
            if iscoroutinefunction(base_class_instance.after_started):
                async def after_started_coro(instance: IRootRunner):
                    await instance.after_started(__module_delegate)
                    return instance

                return after_started_coro(base_class_instance)
            else:
                base_class_instance.after_started(__module_delegate)

        return base_class_instance

    return __call__


def root(cls: Value = None, /, *, plugins: Plugins = None) -> Type[Value]:
    if plugins is None:
        plugins = []

    def wrapper(_cls) -> Type[Value]:
        return __process_root_decorator(_cls, plugins)

    if cls is None:
        return wrapper

    return wrapper(cls)
