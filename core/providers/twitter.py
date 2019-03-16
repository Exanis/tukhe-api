import html
import twitter
from django.conf import settings
from .base import cached


class TwitterProvider():
    @staticmethod
    def _init_api(account):
        api = twitter.Api(
            consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
            consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
            access_token_key=account.key,
            access_token_secret=account.secret,
            tweet_mode='extended'
        )
        return api

    @staticmethod
    def _format_status(tweet):
        return {
            'id': tweet.id_str,
            'author': {
                'screen_name': tweet.user.screen_name,
                'avatar': tweet.user.profile_image_url,
                'name': tweet.user.name,
                'verified': tweet.user.verified,
                'protected': tweet.user.protected
            },
            'date': tweet.created_at,
            'text': html.unescape(tweet.full_text if tweet.full_text is not None else tweet.text),
            'quoted': TwitterProvider._format_status(tweet.quoted_status) if tweet.quoted_status is not None else None,
            'replying_to': tweet.in_reply_to_screen_name,
            'retweet_count': tweet.retweet_count,
            'user_retweeted': tweet.retweeted,
            'like_count': tweet.favorite_count,
            'user_liked': tweet.favorited,
            'urls': [
                {
                    'short': url.url,
                    'target': url.expanded_url
                } for url in tweet.urls
            ],
            'media': [
                {
                    'display_url': media.display_url,
                    'url': media.url,
                    'media_url': media.media_url_https,
                    'alt': media.ext_alt_text,
                    'type': media.type,
                    'video': media.video_info
                } for media in tweet.media
            ] if tweet.media else [],
            'retweeted_status': TwitterProvider._format_status(tweet.retweeted_status) if tweet.retweeted_status else None
        }

    @staticmethod
    @cached('twitter', 'feed', 60)
    def feed(account):
        api = TwitterProvider._init_api(account)
        timeline = api.GetHomeTimeline(
            count=200,
            trim_user=False,
            include_entities=True
        )
        result = [TwitterProvider._format_status(tweet) for tweet in timeline]
        return result

    @staticmethod
    @cached('twitter', 'notifications', 20)
    def notifications(account):
        api = TwitterProvider._init_api(account)
        notifications = api.GetMentions(count=200)
        result = [
            TwitterProvider._format_status(tweet) for tweet in notifications
        ]
        return result

    @staticmethod
    def like(account, tweet):
        api = TwitterProvider._init_api(account)
        result = api.CreateFavorite(status_id=tweet)
        return [TwitterProvider._format_status(result)]

    @staticmethod
    def dislike(account, tweet):
        api = TwitterProvider._init_api(account)
        result = api.DestroyFavorite(status_id=tweet)
        return [TwitterProvider._format_status(result)]

    @staticmethod
    def retweet(account, tweet):
        api = TwitterProvider._init_api(account)
        api.PostRetweet(tweet)
        original_tweet = api.GetStatus(tweet)
        return [TwitterProvider._format_status(original_tweet)]

    @staticmethod
    def unretweet(account, tweet):
        api = TwitterProvider._init_api(account)
        target_tweet = api.GetStatus(tweet, include_my_retweet=True)
        api.DestroyStatus(target_tweet.current_user_retweet)
        result_tweet = api.GetStatus(tweet)
        return [TwitterProvider._format_status(result_tweet)]

    @staticmethod
    def untweet(account, tweet):
        api = TwitterProvider._init_api(account)
        api.DestroyStatus(tweet)
        return []

    @staticmethod
    def quote(account, tweet_from, tweet_id, message):
        api = TwitterProvider._init_api(account)
        result = api.PostUpdate(
            message,
            attachment_url='https://twitter.com/{}/status/{}'.format(
                tweet_from,
                tweet_id
            )
        )
        return [TwitterProvider._format_status(result)]

    @staticmethod
    def tweet(account, message, file=None):
        api = TwitterProvider._init_api(account)
        if file:
            for f in file:
                if isinstance(f, str):
                    pass
                else:
                    f.mode = 'rb'
        result = api.PostUpdate(message[0], media=file)
        return [TwitterProvider._format_status(result)]
