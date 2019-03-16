from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Dashboard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dashboard')
    icon = models.CharField(max_length=64, default="home")
    order = models.PositiveSmallIntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    layout = JSONField(default=dict)

    class Meta():
        ordering = ['order', 'creation_date']


class Widget(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, default="New widget")
    header = models.BooleanField(default=True)
    type = models.CharField(max_length=255)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    config = JSONField(default=dict)
    accounts = models.ManyToManyField('core.Account')


@receiver(post_save, sender=User)
def create_initial_dashboard(sender, instance, created, **kwargs):
    if created:
        Dashboard.objects.create(user=instance)
