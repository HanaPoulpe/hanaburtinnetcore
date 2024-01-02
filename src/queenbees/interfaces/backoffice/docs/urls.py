from django import urls
from django.conf import settings

from .django import urls as django_urls

urlpatterns = []

if settings.DEBUG:
    urlpatterns.append(urls.path("django/", urls.include(django_urls.urlpatterns)))
