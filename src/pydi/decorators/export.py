from pydi.__internal.helpers import AnnotationOf, validate_pydi_provider

from pydi.constants import _PROVIDER_ANNOTATIONS
from pydi.types import ProviderAnnotation, Value


def export(provide: Value) -> Value:
    validate_pydi_provider(provide)

    provider_annotations = AnnotationOf(provide).get(_PROVIDER_ANNOTATIONS, ProviderAnnotation)
    AnnotationOf(provide).set(_PROVIDER_ANNOTATIONS, ProviderAnnotation(token=provider_annotations.token, scope=provider_annotations.scope,
                                                                        exported=True))
    return provide
