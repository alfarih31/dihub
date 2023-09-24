from unittest import TestCase, main

from A import AModule, GlobalScopedAService, ModuleScopedAService, LocalScopedAService
from B import BModule, BService, IBService
from app import App
from pydi.exceptions import ProviderNotFound
from pydi.types import IModuleDelegate


class AppTest(TestCase):
    A_MODULE_REF: IModuleDelegate
    B_MODULE_REF: IModuleDelegate

    def setUp(self) -> None:
        root_app = App()
        self.B_MODULE_REF = root_app.root_ref[BModule]
        self.A_MODULE_REF = root_app.root_ref[AModule]

    def test_global_scoped_provider(self):
        """Global scoped should be shared"""
        global_scoped_a_service = self.A_MODULE_REF.providers[GlobalScopedAService][0]
        global_scoped_a_service_in_b_module = self.B_MODULE_REF.providers[GlobalScopedAService][0]

        self.assertTrue(global_scoped_a_service.deep_eq(global_scoped_a_service_in_b_module))

    def test_module_scoped_provider(self):
        """Module scoped should be unique within a module"""
        module_scoped_a_service = self.A_MODULE_REF.providers[ModuleScopedAService][0]
        module_scoped_a_service_in_b_module = self.B_MODULE_REF.providers[ModuleScopedAService][0]

        b_service = self.B_MODULE_REF.providers[BService][0].cast(IBService)
        module_scoped_a_service_in_b_service = getattr(b_service, "module_a_service")

        self.assertFalse(module_scoped_a_service.deep_eq(module_scoped_a_service_in_b_module))
        self.assertFalse(module_scoped_a_service.deep_eq(module_scoped_a_service_in_b_service))

        self.assertTrue(module_scoped_a_service_in_b_module.deep_eq(module_scoped_a_service_in_b_service))

    def test_local_scoped_provider(self):
        """Local scoped should be unique"""
        with self.assertRaises(ProviderNotFound):
            var = self.B_MODULE_REF.providers[LocalScopedAService]

        global_scoped_a_service = self.A_MODULE_REF.providers[GlobalScopedAService][0]
        module_scoped_a_service = self.A_MODULE_REF.providers[ModuleScopedAService][0]

        b_service = self.B_MODULE_REF.providers[BService][0].cast(IBService)
        local_scoped_a_service_in_b_service = getattr(b_service, "local_a_service")

        self.assertFalse(global_scoped_a_service.deep_eq(module_scoped_a_service))
        self.assertFalse(module_scoped_a_service.deep_eq(local_scoped_a_service_in_b_service))


if __name__ == "__main__":
    main()
