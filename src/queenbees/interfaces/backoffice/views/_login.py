from typing import Any

from django import http, urls
from django.contrib import auth
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.views import generic as views


class AuthForm(auth_forms.AuthenticationForm):
    pass


class AuthView(auth_views.LoginView):
    form_class = AuthForm

    def get_default_redirect_url(self) -> str:
        return "/"


class LogoutView(views.RedirectView):
    def get_redirect_url(self) -> str:
        return urls.reverse("login")

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponseBase:
        auth.logout(request)

        return super().dispatch(request, *args, **kwargs)
