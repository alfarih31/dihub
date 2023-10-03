import unittest
from collections.abc import Iterable
from unittest.mock import MagicMock

from dihub.__internal.proxies import ProviderProxy
from dihub.decorators import provider
from dihub.exceptions import NotAPyDIProvider, ProviderNotFound

from .provider_delegate import ProviderDelegate


class ProviderDelegateTest(unittest.TestCase):
    def test___init___should_raise_NotAPyDIProvider(self):
        def p(): ...

        providers = [p]
        with self.assertRaises(NotAPyDIProvider):
            ProviderDelegate(providers)

    def test___init___should_append_providers(self):
        @provider
        def p(): ...

        providers = [p]
        expected = ProviderDelegate(providers)
        self.assertEqual(len(expected), 1)

    def test___add___should_concat_providers(self):
        @provider
        def p(): ...

        providers = [p]
        expected = ProviderDelegate(providers)

        others = ProviderDelegate(providers)

        initial = len(expected)

        expected += providers
        self.assertEqual(len(expected), initial + len(providers))

        initial = len(expected)

        expected += others
        self.assertEqual(len(expected), initial + len(others))

    def test_append_should_append_providers(self):
        @provider
        def p(): ...

        providers = [p]
        expected = ProviderDelegate(providers)
        initial = len(expected)

        expected.append(p)
        self.assertEqual(len(expected), initial + 1)

    def test_ProviderDelegate_should_iterable(self):
        self.assertTrue(issubclass(ProviderDelegate, Iterable))

    @staticmethod
    def test_on_boot_should_call_provider_on_boot():
        @provider
        def p(): ...

        providers = [p]
        expected = ProviderDelegate(providers)
        expected[p.__name__][0].on_boot = MagicMock()

        expected.on_boot()
        expected[p.__name__][0].on_boot.assert_called_once()

    @staticmethod
    def test_on_post_boot_should_call_provider_on_post_boot():
        @provider
        def p(): ...

        providers = [p]
        expected = ProviderDelegate(providers)
        expected[p.__name__][0].on_post_boot = MagicMock()

        expected.on_post_boot()
        expected[p.__name__][0].on_post_boot.assert_called_once()

    def test___getitem___should_raise_ProviderNotFound_when_no_token_match(self):
        expected = ProviderDelegate([])
        with self.assertRaises(ProviderNotFound):
            expected['any']

    def test___getitem___should_return_match_provider(self):
        @provider
        def p(): ...

        pd = ProviderDelegate([p])
        expected, _ = pd[p.__name__]

        self.assertIsInstance(expected, ProviderProxy)
        self.assertIs(p, expected.release())

    def test___str___should_return_str(self):
        @provider
        def p(): ...

        pd = ProviderDelegate([p])

        self.assertIsInstance(str(pd), str)

    def test___delitem___should_remove_provider(self):
        @provider
        def p(): ...

        pd = ProviderDelegate([p])

        initial = len(pd)
        del pd["p"]
        self.assertEqual(len(pd), initial - 1)


if __name__ == "__main__":
    unittest.main()
