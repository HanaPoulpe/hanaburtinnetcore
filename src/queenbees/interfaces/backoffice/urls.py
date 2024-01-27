from django import urls

from queenbees.core import urls as core_urls
from queenbees.interfaces.backoffice.content import urls as content_urls

from . import views as bo_views
from .docs import urls as docs_urls

urlpatterns = core_urls.urlpatterns

urlpatterns += [
    urls.path("", bo_views.RootView.as_view(), name="root"),
    urls.path("docs/", urls.include(docs_urls.urlpatterns)),
    urls.path("login/", bo_views.AuthView.as_view(), name="login"),
    urls.path("logout/", bo_views.LogoutView.as_view(), name="logout"),
    urls.path("content/", urls.include(content_urls)),
]
