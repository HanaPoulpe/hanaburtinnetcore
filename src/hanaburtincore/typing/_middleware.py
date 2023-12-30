import abc
from typing import Callable

from django import http


class Middleware(abc.ABC):
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    @abc.abstractmethod
    def __call__(self, request: http.HttpRequest) -> http.HttpResponse:
        raise NotImplementedError(self.__class__.__name__, "__call__")
