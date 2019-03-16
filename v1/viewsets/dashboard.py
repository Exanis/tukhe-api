from dateutil import parser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, decorators, status, response
from core import models, providers
from v1 import serializers


class Dashboard(viewsets.ModelViewSet):
    queryset = models.Dashboard.objects.all()
    serializer_class = serializers.Dashboard

    def get_queryset(self):
        return models.Dashboard.objects.filter(
            user=self.request.user
        )


class Widget(viewsets.ModelViewSet):
    queryset = models.Widget.objects.all()
    serializer_class = serializers.Widget

    def get_queryset(self):
        return models.Widget.objects.filter(
            dashboard__uuid=self.kwargs['dashboard_pk'],
            dashboard__user=self.request.user
        )

    @decorators.action(methods=['POST'], detail=True)
    def link(self, *args, **kwargs):
        widget = self.get_object()
        uuid = self.request.data.get('account', '')
        try:
            widget.accounts.get(uuid=uuid)
            return response.Response(status=status.HTTP_200_OK)
        except models.Account.DoesNotExist:
            account = get_object_or_404(
                models.Account,
                uuid=self.request.data['account'],
                user=self.request.user
            )
            widget.accounts.add(account)
            widget.save()
            return response.Response(status=status.HTTP_201_CREATED)

    @decorators.action(methods=['GET'], detail=True)
    def update_with_auth(self, *args, **kwargs):
        widget = self.get_object()
        (provider, method) = widget.type.split('_')
        result = []
        for account in widget.accounts.all():
            result += providers.route(
                provider,
                method,
                account=account,
                **widget.config
            )
        final = sorted(result, key=lambda item: parser.parse(item['date']), reverse=True)
        return response.Response(data=final)

    @decorators.action(methods=['GET'], detail=True)
    def update_no_auth(self, *args, **kwargs):
        widget = self.get_object()
        (provider, method) = widget.type.split('_')
        result = providers.route(
            provider,
            method,
            **widget.config
        )
        final = sorted(result, key=lambda item: parser.parse(item['date']), reverse=True)
        return response.Response(data=final)

    @decorators.action(methods=['POST'], detail=True)
    def action_with_auth(self, *args, **kwargs):
        widget = self.get_object()
        (provider, _) = widget.type.split('_')
        method = self.request.data.get('action')
        result = []
        params = widget.config
        params.update(self.request.data)
        del params['action']
        for account in widget.accounts.all():
            result += providers.route(
                provider,
                method,
                account=account,
                **params
            )
        return response.Response(data=result)

    @decorators.action(methods=['POST'], detail=True)
    def action_no_auth(self, *args, **kwargs):
        widget = self.get_object()
        (provider, _) = widget.type.split('_')
        method = self.request.data.get('action')
        params = widget.config
        params.update(self.request.data)
        del params['action']
        result = providers.route(
            provider,
            method,
            **params
        )
        return response.Response(data=result)
