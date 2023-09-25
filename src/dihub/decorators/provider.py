from inspect import isfunction

from dihub.__internal.helpers import AnnotationOf
from dihub.__internal.proxies import PrimitiveProxy
from dihub.constants import ProviderScope, _PROVIDER_ANNOTATIONS, ROOT_MODULE_DELEGATE
from dihub.exceptions import ReservedInjectToken
from dihub.types import InjectToken, Value, ProviderAnnotation


def __process_provider_decorator(provide: Value, token: InjectToken, scope: ProviderScope):
    if isfunction(provide):
        provide = PrimitiveProxy(provide.__name__, provide())

    final_token = token
    if final_token is None:
        if isinstance(provide, PrimitiveProxy):
            final_token = provide.__name__
        elif isinstance(provide, type):
            final_token = provide.__name__
        else:
            final_token = provide.__class__.__name__

    if final_token == ROOT_MODULE_DELEGATE:
        raise ReservedInjectToken(final_token)

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
