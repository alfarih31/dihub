from typing import Any

from pydi.constants import _PROVIDER_ANNOTATIONS, _MODULE_ANNOTATIONS
from pydi.exceptions import NotAPyDIProvider, NotAPyDIModule
from pydi.types import ProviderAnnotation, ModuleAnnotation
from .annotation_of import AnnotationOf


def __generic_validate_pydi(t: Any, ann_name: str, expected_type: Any, not_match_exception: Exception):
    try:
        if AnnotationOf(t).get(ann_name, expected_type) is None:
            raise not_match_exception
    except ValueError:
        raise not_match_exception


def validate_pydi_provider(t: Any):
    __generic_validate_pydi(t, _PROVIDER_ANNOTATIONS, ProviderAnnotation, NotAPyDIProvider(str(t)))


def validate_pydi_module(t: Any):
    __generic_validate_pydi(t, _MODULE_ANNOTATIONS, ModuleAnnotation, NotAPyDIModule(str(t)))
