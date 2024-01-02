from django.views.generic import base

TEMPLATE_ROOT = "docs/django/"


def _make_template_name(name: str) -> str:
    return TEMPLATE_ROOT + name + ".html"


class StylingView(base.TemplateView):
    template_name = _make_template_name("styling")
