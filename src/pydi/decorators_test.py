import unittest
from unittest.mock import MagicMock

from pydi.__internal.delegates import InjectedDelegate
from pydi.constants import _MODULE_ANNOTATIONS, _PROVIDER_ANNOTATIONS
from pydi.decorators import module, inject, provider, root, export, for_root
from pydi.exceptions import NotAPyDIModule, NotAPyDIProvider
from pydi.types import ModuleAnnotation, ProviderAnnotation


class DecoratorsTest(unittest.TestCase):
    def test_module_decorator_should_set_module_annotation(self):
        @module()
        class C: ...

        self.assertIn(_MODULE_ANNOTATIONS, C.__annotations__)
        self.assertIsInstance(C.__annotations__[_MODULE_ANNOTATIONS], ModuleAnnotation)

        default_annotation = ModuleAnnotation(imports=[], providers=[])
        self.assertEqual(default_annotation, C.__annotations__[_MODULE_ANNOTATIONS])

    def test_inject_should_return_InjectedDelegate(self):
        class C:
            member: str = inject("token")

        c = C()
        self.assertIsInstance(c.member, InjectedDelegate)
        self.assertEqual(c.member.token, "token")

    def test_provider_decorator_should_set_provider_annotation(self):
        @provider("token")
        class C: ...

        self.assertIn(_PROVIDER_ANNOTATIONS, C.__annotations__)
        self.assertIsInstance(C.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)

        @provider("provide")
        def constant_provider() -> str: ...

        self.assertIn(_PROVIDER_ANNOTATIONS, constant_provider.__annotations__)
        self.assertIsInstance(constant_provider.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)

    def test_root_decorator_should_raise_NotAPyDIModule_to_non_module(self):
        with self.assertRaises(NotAPyDIModule):
            @root
            class C: ...

    def test_root_decorator_should_wrap_a_class(self):
        class OC: ...

        # Implicitly decorate
        C = module()(OC)
        C = root(C)

        self.assertIsInstance(C, root)

        c = C()
        self.assertIsInstance(c, OC)

    def test_root_decorator_should_not_affect_the_actual_class(self):
        class OC:
            def __init__(self, an_arg: int): ...

            def a_method(self): ...

        OC.a_method = MagicMock()
        OC.__init__ = MagicMock(return_value=None)

        # Implicitly decorate
        C = module()(OC)
        C = root(C)

        c = C(an_arg=1)
        OC.__init__.assert_called_once_with(an_arg=1)

        c.a_method()
        OC.a_method.assert_called_once()

    def test_export_decorator_should_set_annotation_to_exported(self):
        @export
        @provider(token="token")
        class C: ...

        annotations: ProviderAnnotation = C.__annotations__.get(_PROVIDER_ANNOTATIONS)
        self.assertIs(annotations.exported, True)

    def test_export_decorator_should_raise_NotAPyDIProvider_to_non_provider(self):
        with self.assertRaises(NotAPyDIProvider):
            @export
            class C: ...

    def test_for_root_decorator_should_set_annotation_to_for_root(self):
        @for_root
        @module()
        class C: ...

        annotations: ModuleAnnotation = C.__annotations__.get(_MODULE_ANNOTATIONS)
        self.assertIs(annotations.for_root, True)

    def test_export_decorator_should_raise_NotAPyDIModule_to_non_module(self):
        with self.assertRaises(NotAPyDIModule):
            @for_root
            class C: ...


if __name__ == "__main__":
    unittest.main()