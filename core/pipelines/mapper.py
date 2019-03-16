from core import mappers, models


def map_social_to_account(backend, user, response, *args, **kwargs):
    mapper = getattr(mappers, 'map_{}'.format(backend.name))
    (id, name, key, secret) = mapper(response)
    try:
        account = models.Account.objects.get(identifier=id, user=user, provider=backend.name)
        account.name = name
        account.key = key
        account.secret = secret
        account.save()
    except models.Account.DoesNotExist:
        models.Account.objects.create(
            user=user,
            identifier=id,
            provider=backend.name,
            name=name,
            key=key,
            secret=secret
        )
