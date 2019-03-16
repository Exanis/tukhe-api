from django.test import TestCase
from core import mappers


class MappersTestCase(TestCase):
    def test_oauth_mapper_twitter(self):
        response = {
            'access_token': {
                'screen_name': 'test',
                'oauth_token': 'oauth_token_test',
                'oauth_token_secret': 'oauth_token_secret_test'
            },
            'id': 3
        }
        result = mappers.map_twitter(response)
        self.assertEquals(result[0], 3)
        self.assertEquals(result[1], '@test')
        self.assertEquals(result[2], 'oauth_token_test')
        self.assertEquals(result[3], 'oauth_token_secret_test')
