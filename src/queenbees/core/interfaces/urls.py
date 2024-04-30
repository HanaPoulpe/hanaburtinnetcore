from django import urls

urlpatterns = [
    urls.path("health/", urls.include("health_check.urls")),
]
