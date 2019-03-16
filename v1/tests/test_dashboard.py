from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from core import models


class DashboardTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        user2 = get_user_model().objects.create(username='test2')
        self.dashboard = models.Dashboard.objects.create(
            user=self.user,
            icon='test'
        )
        dashboard2 = models.Dashboard.objects.create(
            user=user2,
            icon='test2'
        )
        self.widget = models.Widget.objects.create(
            dashboard=self.dashboard,
            type='test_widget'
        )
        models.Widget.objects.create(
            dashboard=dashboard2,
            type='test_widget2'
        )
        self.client.force_authenticate(self.user)

    def test_dashboard_queryset(self):
        result = self.client.get('/api/v1/dashboard/')
        self.assertEqual(
            len(result.json()),
            2
        )

    def test_widget_queryset(self):
        result = self.client.get('/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/')
        self.assertEqual(
            len(result.json()),
            1
        )

    def test_widget_link(self):
        account = models.Account.objects.create(
            user=self.user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        result_not_existing = self.client.post(
            '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/link/',
            {
                'account': account.uuid
            }
        )
        self.assertEqual(result_not_existing.status_code, 201)
        result_existing = self.client.post(
            '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/link/',
            {
                'account': account.uuid
            }
        )
        self.assertEqual(result_existing.status_code, 200)

    def test_update_with_auth(self):
        account = models.Account.objects.create(
            user=self.user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        with patch('v1.viewsets.dashboard.providers.route') as method:
            method.return_value = [{
                'date': '2019-01-28'
            }]
            self.client.post(
                '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/link/',
                {
                    'account': account.uuid
                }
            )
            result = self.client.get('/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/update_with_auth/')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(len(result.json()), 1)

    def test_update_without_auth(self):
        with patch('v1.viewsets.dashboard.providers.route') as method:
            method.return_value = [{
                'date': '2019-01-28'
            }]
            result = self.client.get('/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/update_no_auth/')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(len(result.json()), 1)

    def test_action_with_auth(self):
        account = models.Account.objects.create(
            user=self.user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        with patch('v1.viewsets.dashboard.providers.route') as method:
            method.return_value = [{
                'date': '2019-01-28'
            }]
            self.client.post(
                '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/link/',
                {
                    'account': account.uuid
                }
            )
            result = self.client.post(
                '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/action_with_auth/',
                {
                    'action': 'test',
                    'param1': 'param'
                }
            )
            self.assertEqual(result.status_code, 200)
            self.assertEqual(len(result.json()), 1)

    def test_action_no_auth(self):
        with patch('v1.viewsets.dashboard.providers.route') as method:
            method.return_value = [{
                'date': '2019-01-28'
            }]
            result = self.client.post(
                '/api/v1/dashboard/' + self.dashboard.uuid.hex + '/widget/' + self.widget.uuid.hex + '/action_no_auth/',
                {
                    'action': 'test',
                    'param1': 'param'
                }
            )
            self.assertEqual(result.status_code, 200)
            self.assertEqual(len(result.json()), 1)
