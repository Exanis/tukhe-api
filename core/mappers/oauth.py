def map_twitter(response):
    data = response['access_token']
    return (
        response['id'],
        '@{}'.format(data['screen_name']),
        data['oauth_token'],
        data['oauth_token_secret']
    )
