from pydi.__internal.helpers import AnnotationOf, validate_pydi_module

from pydi.constants import _MODULE_ANNOTATIONS
from pydi.types import ModuleAnnotation, _Instance


def for_root(m: _Instance) -> _Instance:
    validate_pydi_module(m)

    module_annotations = AnnotationOf(m).get(_MODULE_ANNOTATIONS, ModuleAnnotation)
    AnnotationOf(m).set(_MODULE_ANNOTATIONS, ModuleAnnotation(imports=module_annotations.imports, providers=module_annotations.providers,
                                                              for_root=True))

    return m
