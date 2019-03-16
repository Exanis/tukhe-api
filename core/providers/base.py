from functools import wraps
from datetime import timedelta
from django.utils import timezone
from core import models


def cached(provider, key, expiration_time):
    def decorator(target):
        @wraps(target)
        def update_from_cache(*args, **kwargs):
            if 'account' not in kwargs:
                raise Exception('Account must be an arg of cached function')
            models.CachedRequestResult.objects.filter(expire_date__lt=timezone.now()).delete()
            try:
                result = models.CachedRequestResult.objects.get(
                    account=kwargs['account'],
                    provider=provider,
                    key=key,
                )
                return result.result
            except models.CachedRequestResult.DoesNotExist:
                result = target(*args, **kwargs)
                models.CachedRequestResult.objects.create(
                    account=kwargs['account'],
                    provider=provider,
                    key=key,
                    result=result,
                    expire_date=timezone.now() + timedelta(seconds=expiration_time)
                )
            return result
        return update_from_cache
    return decorator


def route(provider, method, *args, **kwargs):
    from .twitter import TwitterProvider
    from .misc import MiscProvider


    PROVIDERS = {
        'twitter': TwitterProvider,
        'misc': MiscProvider
    }

    if provider not in PROVIDERS or not hasattr(PROVIDERS[provider], method):
        return None
    target = getattr(PROVIDERS[provider], method)
    result = target(*args, **kwargs)
    return result
