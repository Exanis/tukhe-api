from uuid import uuid4
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import JSONField


class Account(models.Model):
    TYPE_TWITTER = 'twitter'
    POSSIBLE_TYPES = [
        (TYPE_TWITTER, 'Twitter',),
    ]

    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='accounts')
    identifier = models.CharField(max_length=255, default='')
    provider = models.CharField(max_length=15, choices=POSSIBLE_TYPES)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta():
        ordering = ['creation_date']


class CachedRequestResult(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cache')
    provider = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    creation_date = models.DateTimeField(default=timezone.now)
    result = JSONField()
    expire_date = models.DateTimeField()
