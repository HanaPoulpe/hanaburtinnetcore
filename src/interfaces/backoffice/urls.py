from django import urls
from django.contrib import admin

from hanaburtincore import urls as core_urls

from .docs import urls as docs_urls

urlpatterns = core_urls.urlpatterns

urlpatterns += [
    urls.path("admin/", admin.site.urls),
    urls.path("docs/", urls.include(docs_urls.urlpatterns)),
]
