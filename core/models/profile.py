from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    tutorial = models.BooleanField(default=True)


@receiver(post_save, sender=get_user_model())
def create_initial_dashboard(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
