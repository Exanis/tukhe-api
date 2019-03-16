from rest_framework import viewsets, response, status
from core import models
from v1 import serializers


class Account(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.Account

    def get_queryset(self):
        return self.request.user.accounts.all()

    def create(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def partial_update(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_501_NOT_IMPLEMENTED)
