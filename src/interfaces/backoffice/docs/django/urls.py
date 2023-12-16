from django import urls

from . import views

urlpatterns = [urls.path("styling", view=views.StylingView.as_view())]
