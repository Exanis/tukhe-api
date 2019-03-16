from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from core import models


class AccountTestCase(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='user')
        user2 = get_user_model().objects.create(username='user2')
        self.account = models.Account.objects.create(
            user=user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        models.Account.objects.create(
            user=user2,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        self.client.force_authenticate(user)

    def test_queryset(self):
        result = self.client.get('/api/v1/account/')
        self.assertEqual(
            len(result.json()),
            1
        )

    def test_create(self):
        result = self.client.post('/api/v1/account/')
        self.assertEqual(result.status_code, 501)

    def test_update(self):
        result = self.client.put('/api/v1/account/' + self.account.uuid.hex + '/')
        self.assertEqual(result.status_code, 501)

    def test_partial_update(self):
        result = self.client.patch('/api/v1/account/' + self.account.uuid.hex + '/')
        self.assertEqual(result.status_code, 501)
