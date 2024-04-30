from django import http, urls

from queenbees.core import typing

UNAUTHENTICATED_URLS: set[str] = {"login", "health_check:health_check_home"}


class AuthRequiredMiddleware(typing.Middleware):
    def __call__(self, request: http.HttpRequest) -> http.HttpResponse:
        if self._check_unauthentiated_url(request.path):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(urls.reverse("login"))

        return self.get_response(request)

    def _check_unauthentiated_url(self, path: str) -> bool:
        if path.startswith("health"):
            return True

        for url in UNAUTHENTICATED_URLS:
            if path == urls.reverse(url):
                return True

        return False
