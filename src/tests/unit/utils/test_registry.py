import functools
from collections.abc import Callable

import attrs
import pytest

from queenbees.utils import registry


class TestRegistry:
    def test_registry(self) -> None:
        r: registry.Registry[str, Callable[[], int]] = registry.Registry()
        r.register("one", lambda: 1)

        @r("two")
        def two() -> int:
            return 2

        assert r["one"]() == 1
        assert r["two"]() == 2
        assert r.get("two", default=lambda: 3)() == 2

        assert r.get("three", default=lambda: 3)() == 3
        assert r.get("three") is None
        with pytest.raises(KeyError):
            r["three"]

        ref = {"one": 1, "two": 2}
        for number, name in r:
            assert number() == ref.pop(name)

        assert ref == {}


class TestNamedRegistry:
    def test_named_registry(self) -> None:
        r = registry.NamedRegistry()

        @r
        class Base:
            pass

        @r()
        class Second:
            pass

        assert r["Base"] is Base
        assert r["Second"] is Second
        assert r.get("Base", default=Second) is Base

        assert set(r) == {(Base, "Base"), (Second, "Second")}
