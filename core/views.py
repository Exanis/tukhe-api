from django.shortcuts import redirect
from django.conf import settings


def index(request):
    url = "{}?{}".format(
        settings.AUTH_REDIRECT_URL,
        request.GET.urlencode()
    )
    return redirect(url)
