import contextlib
import functools
import os
import pathlib
import subprocess
from collections.abc import Callable, Generator
from typing import ParamSpec, TypeAlias, TypeVar, overload

Path: TypeAlias = int | str | bytes | pathlib.Path | os.PathLike[str] | os.PathLike[bytes]


@contextlib.contextmanager
def chdir(path: Path) -> Generator[None, None, None]:
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)


PROJECT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",  # src
        "..",  # project
    )
)
SRC_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "src"))


@contextlib.contextmanager
def cwd_project() -> Generator[None, None, None]:
    with chdir(PROJECT_DIR):
        yield


@contextlib.contextmanager
def cwd_src() -> Generator[None, None, None]:
    with chdir(SRC_DIR):
        yield


_P = ParamSpec("_P")
_T = TypeVar("_T")


@overload
def sub_command_wrapper(_fnc: Callable[_P, None]) -> Callable[_P, None]: ...


@overload
def sub_command_wrapper() -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...


def sub_command_wrapper(
    _fnc: Callable[_P, _T] | None = None
) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    if not _fnc:
        return sub_command_wrapper  # type: ignore

    @functools.wraps(_fnc)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        try:
            return _fnc(*args, **kwargs)
        except subprocess.CalledProcessError:
            exit(2)

    return wrapper
