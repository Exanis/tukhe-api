from django.urls import path, include
from rest_framework_nested import routers
from v1 import viewsets


router = routers.SimpleRouter()
router.register('dashboard', viewsets.Dashboard)
router.register('account', viewsets.Account)

widget_router = routers.NestedSimpleRouter(router, 'dashboard', lookup='dashboard')
widget_router.register('widget', viewsets.Widget)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(widget_router.urls))
]
