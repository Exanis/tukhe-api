from django.test import TestCase
from django.conf import settings


class ViewsTestCase(TestCase):
    def test_index_view(self):
        result = self.client.get('/?test=val', follow=False)
        self.assertRedirects(
            result,
            settings.AUTH_REDIRECT_URL + '?test=val',
            fetch_redirect_response=False
        )
