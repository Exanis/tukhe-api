from rest_framework import serializers
from core import models


class Account(serializers.ModelSerializer):
    class Meta():
        fields = [
            'uuid',
            'provider',
            'name'
        ]
        model = models.Account
