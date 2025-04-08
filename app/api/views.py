from django.contrib.auth import get_user_model
from django.http import HttpResponse


def status(request):
    # DB Health check
    get_user_model().objects.exists()
    return HttpResponse("")