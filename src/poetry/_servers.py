import contextlib
import functools
import multiprocessing
import os
import sys
from collections.abc import Callable, Generator
from typing import TypeAlias

import manage

from . import _general as general
from . import _utils as utils

Runner: TypeAlias = Callable[[], None]


@contextlib.contextmanager
def _with_frontend() -> Generator[None, None, None]:
    if not os.environ.get("LOCALDEV"):
        yield
        return

    frontend = multiprocessing.Process(
        target=general.build_frontend,
        kwargs={"set_watcher_mode": True},
    )
    frontend.start()
    yield
    frontend.terminate()
    frontend.join()


def _setup_django(configuration: str) -> Callable[[Runner], Runner]:
    def wrapper(fnc: Runner) -> Runner:
        @functools.wraps(fnc)
        def wraps() -> None:
            os.environ["DJANGO_CONFIGURATION"] = configuration
            with utils.cwd_src():  # type: ignore
                if not os.path.exists(".env"):
                    with open(".env", "w"):
                        print(".env file not found, creating an empty one.")

                fnc()

        return wraps

    return wrapper


def run_server(port: int = 8000) -> None:
    manage.main("poetry-run", "runserver", f"0.0.0.0:{port}", *sys.argv[1:])


@_setup_django("Backoffice")
def run_backoffice_server() -> None:
    with _with_frontend():
        run_server(8000)


@_setup_django("Api")
def run_api_server() -> None:
    run_server(8001)
