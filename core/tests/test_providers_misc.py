from django.test import TestCase
from core import providers
from .tools import snapshot


class FakeRssElement():
    id = 123
    title = "test title"
    link = "test"
    published = "test date"


class FakeFeed():
    entries = [FakeRssElement()]


class ProvidersMiscTestCase(TestCase):
    @staticmethod
    @snapshot('feedparser.parse', 'providers_misc_rss')
    def test_rss(patch_function):
        patch_function.return_value = FakeFeed()
        result = providers.route(
            'misc',
            'rss',
            url='test url'
        )
        assert(result == [
            {
                "id": 123,
                "href": "test",
                "title": "test title",
                "date": "test date"
            }
        ])

