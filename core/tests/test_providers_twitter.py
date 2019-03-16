from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models, providers
from .tools import snapshot, local_snapshot


class FakeTweet():
    class FakeUser():
        screen_name = 'test_screen_name'
        profile_image_url = 'test_image'
        name = 'test_name'
        verified = True
        protected = False

    class FakeUrl():
        url = 'test url'
        expanded_url = 'test expanded url'

    class FakeMedia():
        display_url = 'test display url'
        url = 'test url'
        media_url_https = 'test https'
        ext_alt_text = 'test alt'
        type = 'test type'
        video_info = 'test video info'

    def __init__(self):
        self.id_str = 'test id'
        self.user = FakeTweet.FakeUser()
        self.created_at = 'test date'
        self.full_text = 'test text'
        self.text = 'test'
        self.quoted_status = None
        self.in_reply_to_screen_name = 'test reply'
        self.retweet_count = 3
        self.retweeted = False
        self.favorite_count = 2
        self.favorited = True
        self.urls = [FakeTweet.FakeUrl()]
        self.media = [FakeTweet.FakeMedia()]
        self.retweeted_status = None
        self.current_user_retweet = 'test current user retweet'


class FakeFile():
    mode = 'r'


class FakeTwitterApi():
    def __init__(self):
        self.called = []

    def GetHomeTimeline(self, *args, **kwargs):
        fakeTweet1 = FakeTweet()
        fakeTweet2 = FakeTweet()

        fakeTweet2.full_text = None
        fakeTweet2.quoted_status = fakeTweet1
        fakeTweet2.media = None
        fakeTweet2.retweeted_status = fakeTweet1
        self.called.append('GetHomeTimeline')
        return [fakeTweet1, fakeTweet2]

    def GetMentions(self, *args, **kwargs):
        self.called.append('GetMentions')
        return [FakeTweet()]

    def CreateFavorite(self, *args, **kwargs):
        self.called.append('CreateFavorite')
        return FakeTweet()

    def DestroyFavorite(self, *args, **kwargs):
        self.called.append('DestroyFavorite')
        return FakeTweet()

    def PostRetweet(self, *args, **kwargs):
        self.called.append('PostRetweet')

    def GetStatus(self, *args, **kwargs):
        self.called.append('GetStatus')
        return FakeTweet()

    def DestroyStatus(self, *args, **kwargs):
        self.called.append('DestroyStatus')

    def PostUpdate(self, *args, **kwargs):
        self.called.append('PostUpdate')
        return FakeTweet()

class ProviderTwitterTestCase(TestCase):
    @staticmethod
    @snapshot('twitter.Api', 'providers_twitter_feed')
    def test_provider_methods(mock_method):
        user = get_user_model().objects.create(username='test')
        account = models.Account.objects.create(
            user=user,
            identifier='test',
            provider='twitter',
            name='@test',
            key='key-test',
            secret='secret-test'
        )
        methods = {
            'feed': {
                'call': ['GetHomeTimeline'],
                'args': {
                    'account': account
                }
            },
            'notifications': {
                'call': ['GetMentions'],
                'args': {
                    'account': account
                }
            },
            'like': {
                'call': ['CreateFavorite'],
                'args': {
                    'account': account,
                    'tweet': 'test'
                }
            },
            'dislike': {
                'call': ['DestroyFavorite'],
                'args': {
                    'account': account,
                    'tweet': 'test'
                }
            },
            'retweet': {
                'call': ['PostRetweet', 'GetStatus'],
                'args': {
                    'account': account,
                    'tweet': 'test'
                }
            },
            'unretweet': {
                'call': ['GetStatus', 'DestroyStatus', 'GetStatus'],
                'args': {
                    'account': account,
                    'tweet': 'test'
                }
            },
            'untweet': {
                'call': ['DestroyStatus'],
                'args': {
                    'account': account,
                    'tweet': 'test'
                }
            },
            'quote': {
                'call': ['PostUpdate'],
                'args': {
                    'account': account,
                    'tweet_from': 'me',
                    'tweet_id': 'test',
                    'message': 'test message'
                }
            },
            'tweet': {
                'call': ['PostUpdate'],
                'args': {
                    'account': account,
                    'message': 'test',
                    'file': [
                        'test',
                        FakeFile()
                    ]
                }
            }
        }
        for method in methods:
            fakeApi = FakeTwitterApi()
            mock_method.return_value = fakeApi
            args = methods[method]['args']
            result = providers.route(
                'twitter',
                method,
                **args
            )
            local_snapshot('providers_twitter_result', method, result)
            assert(methods[method]['call'] == fakeApi.called)
