from dihub.__internal.helpers import AnnotationOf, validate_dihub_module

from dihub.constants import _MODULE_ANNOTATIONS
from dihub.types import ModuleAnnotation, Instance


def for_root(m: Instance) -> Instance:
    validate_dihub_module(m)

    module_annotations = AnnotationOf(m).get(_MODULE_ANNOTATIONS, ModuleAnnotation)
    AnnotationOf(m).set(_MODULE_ANNOTATIONS, ModuleAnnotation(imports=module_annotations.imports, providers=module_annotations.providers,
                                                              for_root=True))

    return m
