import unittest
from typing import Annotated, get_type_hints
from unittest.mock import MagicMock, AsyncMock

from dihub.__internal.delegates import InjectedDelegate
from dihub.constants import _MODULE_ANNOTATIONS, _PROVIDER_ANNOTATIONS, ROOT_MODULE_DELEGATE
from dihub.decorators import module, inject, provider, root, export, for_root
from dihub.exceptions import NotAPyDIModule, NotAPyDIProvider, ReservedInjectToken
from dihub.types import ModuleAnnotation, ProviderAnnotation, IRootPlugin, IRootRunner, IModuleDelegate


class DecoratorsTest(unittest.IsolatedAsyncioTestCase):
    def test_module_decorator_should_set_module_annotation(self):
        @module
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

    def test_inject_should_working_with_annotated(self):
        class C:
            member: Annotated[str, inject("token")]

        hints = get_type_hints(C, include_extras=True)
        self.assertIn("member", hints)

    def test_provider_decorator_should_set_provider_annotation(self):
        @provider(token="token")
        class C: ...

        self.assertIn(_PROVIDER_ANNOTATIONS, C.__annotations__)
        self.assertIsInstance(C.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)

        @provider(token="provide")
        def constant_provider() -> str: ...

        self.assertIn(_PROVIDER_ANNOTATIONS, constant_provider.__annotations__)
        self.assertIsInstance(constant_provider.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)

        @provider
        class B: ...

        self.assertIn(_PROVIDER_ANNOTATIONS, B.__annotations__)
        self.assertIsInstance(B.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)
        self.assertIs(B.__annotations__[_PROVIDER_ANNOTATIONS].token, B.__name__)

        b = B()
        provider(b)
        self.assertIn(_PROVIDER_ANNOTATIONS, b.__annotations__)
        self.assertIsInstance(b.__annotations__[_PROVIDER_ANNOTATIONS], ProviderAnnotation)
        self.assertIs(b.__annotations__[_PROVIDER_ANNOTATIONS].token, b.__class__.__name__)

    def test_provider_decorator_should_raise_ReservedInjectToken(self):
        with self.assertRaises(ReservedInjectToken):
            @provider(token=ROOT_MODULE_DELEGATE)
            class B: ...

    def test_root_decorator_should_raise_NotAPyDIModule_to_non_module(self):
        with self.assertRaises(NotAPyDIModule):
            @root
            class C: ...

    def test_root_decorator_should_not_affect_class_initialization(self):
        class OC: ...

        # Implicitly decorate
        C = module()(OC)
        C = root(C)

        c1 = C()
        self.assertIsInstance(c1, OC)

        c2 = C()
        self.assertIsInstance(c2, OC)

        self.assertNotEqual(c1, c2)

    def test_root_decorator_should_wrap_a_class(self):
        class OC: ...

        # Implicitly decorate
        C = module()(OC)
        C = root(C)

        c = C()
        self.assertIsInstance(c, OC)

    def test_root_decorator_should_call_plugin(self):
        class Plugin(IRootPlugin):
            def __call__(self, *args, **kwargs):
                pass

        Plugin.__call__ = MagicMock()

        class OC: ...

        # Implicitly decorate
        C = module()(OC)
        C = root(C, plugins=[Plugin()])

        c = C()
        Plugin.__call__.assert_called_once()

    async def test_root_decorator_should_after_started(self):
        class OC(IRootRunner):
            async def after_started(self, root_module_delegate: IModuleDelegate):
                pass

        OC.after_started = AsyncMock()

        # Implicitly decorate
        C = module()(OC)
        C = root()(C)

        c = C()
        await c
        OC.after_started.assert_called_once()

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
        @module
        class C: ...

        annotations: ModuleAnnotation = C.__annotations__.get(_MODULE_ANNOTATIONS)
        self.assertIs(annotations.for_root, True)

    def test_export_decorator_should_raise_NotAPyDIModule_to_non_module(self):
        with self.assertRaises(NotAPyDIModule):
            @for_root
            class C: ...


if __name__ == "__main__":
    unittest.main()
