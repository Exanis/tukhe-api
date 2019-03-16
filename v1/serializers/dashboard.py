from rest_framework import serializers
from core import models


class Widget(serializers.ModelSerializer):
    dashboard = serializers.PrimaryKeyRelatedField(
        queryset=models.Dashboard.objects.all(),
        write_only=True
    )

    class Meta():
        fields = [
            'uuid',
            'dashboard',
            'title',
            'header',
            'type',
            'config'
        ]
        model = models.Widget


class Dashboard(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta():
        fields = [
            'uuid',
            'icon',
            'layout',
            'user'
        ]
        model = models.Dashboard
