from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from core.providers.base import route, cached


def test_func(account, i):
    return i


class ProvidersBaseTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='test')
        self.account = models.Account.objects.create(
            user=user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        decorator = cached('test', '123', 3600)
        self.decorated = decorator(test_func)

    def test_cached_no_account(self):
        try:
            self.decorated()
            self.assertFalse(True, 'Should have raised for no account')
        except Exception:
            pass

    def test_cached_account(self):
        self.decorated(account=self.account, i=2)
        self.assertEqual(
            len(models.CachedRequestResult.objects.all()),
            1
        )
        self.assertEqual(self.decorated(account=self.account, i=3), 2)

    def test_router_no_provider(self):
        self.assertIsNone(route('not_existing', 'test'))
        self.assertIsNone(route('misc', 'not_existing'))
