import abc
from collections.abc import Callable, Hashable, Iterator
from typing import Generic, Protocol, TypeVar, overload

_T = TypeVar("_T")
_ID = TypeVar("_ID", bound=Hashable, contravariant=True)


class Registry(Generic[_ID, _T], abc.ABC):
    """
    Represent a registry of objects.

    >>> from queenbees.utils import registry

    >>> my_numbers: registry.Registry[str, Callable[[], int]] = registry.Registry()
    >>> my_numbers.register("one", lambda: 1)

    >>> @my_numbers("two")
    >>> def two() -> int:
    >>>     return 2

    >>> for numbers, name in my_numbers:
    >>>     print(name, numbers())
    <<< one 1
    <<< two 2

    >>> my_numbers["one"]()
    <<< 1

    >>> my_numbers.get("three", lambda: 3)()
    <<< 3
    """

    _registry: dict[_ID, _T] | None = None

    def __call__(self, name: _ID) -> Callable[[_T], _T]:
        def wrapper(obj: _T) -> _T:
            self.register(name, obj)
            return obj

        return wrapper

    def register(self, name: _ID, obj: _T) -> None:
        if self._registry is None:
            self._registry = {}
        self._registry[name] = obj

    def __iter__(self) -> Iterator[tuple[_T, _ID]]:
        class It(Iterator[tuple[_T, _ID]]):
            def __init__(self, iterable: dict[_ID, _T]) -> None:
                self._it = iter(iterable.items())

            def __next__(self) -> tuple[_T, _ID]:
                name, obj = next(self._it)
                return obj, name

        return It(self._registry or {})

    def __len__(self) -> int:
        if not self._registry:
            return 0

        return len(self._registry)

    def __getitem__(self, item: _ID) -> _T:
        if not self._registry:
            raise KeyError(item)

        return self._registry[item]

    def get(self, item: _ID, *, default: _T | None = None) -> _T | None:
        if not self._registry:
            return default

        return self._registry.get(item, default)


class _N(Protocol):
    @property
    def __name__(self) -> str:
        return self.__name__


class NamedRegistry(_N):
    """
    Represent a registry of named objects.

    Works the same way as :class:`Registry`, but the objects are named.
    """

    def __init__(self) -> None:
        self._registry: Registry = Registry()

    @overload
    def __call__(self) -> Callable[[_N], _N]: ...

    @overload
    def __call__(self, obj: _N) -> _N: ...

    def __call__(self, obj: _N | None = None) -> Callable[[_N], _N] | _N:
        if obj is not None:
            self.register(obj)
            return obj

        def wrapper(_obj: _N) -> _N:
            self.register(_obj)
            return _obj

        return wrapper

    def register(self, obj: _N) -> None:
        self._registry.register(obj.__name__, obj)

    def __iter__(self) -> Iterator[tuple[_N, str]]:
        return iter(self._registry)

    def __len__(self) -> int:
        return len(self._registry)

    def __getitem__(self, item: str) -> _N:
        return self._registry[item]

    def get(self, item: str, *, default: _N | None = None) -> _N | None:
        return self._registry.get(item, default=default)
