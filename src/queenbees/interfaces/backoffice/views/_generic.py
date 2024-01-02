from typing import Any

from django import http, urls
from django.views import generic


class RootView(generic.TemplateView):
    template_name = "index.html"
