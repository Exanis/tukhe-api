from django.test import TestCase
from django.contrib.auth import get_user_model
from core import pipelines, models


class FakeBackend():
    name = 'twitter'


class PipelineTestCase(TestCase):
    def test_map_social_to_new_account(self):
        user = get_user_model().objects.create(username='test')
        response = {
            'access_token': {
                'screen_name': 'test',
                'oauth_token': 'oauth_token_test',
                'oauth_token_secret': 'oauth_token_secret_test'
            },
            'id': 3
        }

        self.assertEquals(len(models.Account.objects.all()), 0)
        pipelines.map_social_to_account(
            FakeBackend(),
            user,
            response
        )
        self.assertEquals(len(models.Account.objects.all()), 1)

    def test_map_social_to_existing_account(self):
        user = get_user_model().objects.create(username='test')
        response = {
            'access_token': {
                'screen_name': 'test',
                'oauth_token': 'oauth_token_test',
                'oauth_token_secret': 'oauth_token_secret_test'
            },
            'id': 3
        }
        pipelines.map_social_to_account(
            FakeBackend(),
            user,
            response
        )
        response['access_token']['screen_name'] = 'new test'
        pipelines.map_social_to_account(
            FakeBackend(),
            user,
            response
        )
        self.assertEquals(len(models.Account.objects.all()), 1)
        self.assertEquals(len(models.Account.objects.filter(name='@new test')), 1)
