from inspect import isfunction

from pydi.__internal.helpers import AnnotationOf

from pydi.__internal.proxies import PrimitiveProxy
from pydi.constants import ProviderScope, _PROVIDER_ANNOTATIONS
from pydi.types import InjectToken, Value, ProviderAnnotation


def __process_provider_decorator(provide: Value, token: InjectToken, scope: ProviderScope):
    if isfunction(provide):
        provide = PrimitiveProxy(provide())

    final_token = token
    if final_token is None:
        if isinstance(provide, type):
            final_token = provide.__name__
        else:
            final_token = provide.__class__.__name__

    AnnotationOf(provide).set(_PROVIDER_ANNOTATIONS, ProviderAnnotation(token=final_token, scope=scope))
    return provide


def provider(provide: Value = None, /, *, token: InjectToken = None, scope: ProviderScope = ProviderScope.GLOBAL):
    """
    :param provide: The decorated class
    :param token: Provider injects token. Used to refer the provider upon injection
    :param scope: The provider scopes
    """

    def wrapper(cls: Value) -> Value:
        return __process_provider_decorator(cls, token, scope)

    if provide is None:
        return wrapper

    return wrapper(provide)
