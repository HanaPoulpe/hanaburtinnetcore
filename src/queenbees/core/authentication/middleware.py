from django import http, urls

from queenbees.core import typing


class AuthRequiredMiddleware(typing.Middleware):
    def __call__(self, request: http.HttpRequest) -> http.HttpResponse:
        if request.path == urls.reverse("login"):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(urls.reverse("login"))

        return self.get_response(request)
