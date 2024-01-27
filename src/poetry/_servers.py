import contextlib
import multiprocessing
import os
import sys
from collections.abc import Generator

import manage

from . import _general as general
from . import _utils as utils


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


def run_server(port: int = 8000) -> None:
    manage.main("poetry-run", "runserver", f"0.0.0.0:{port}", *sys.argv[1:])


def run_backoffice_server() -> None:
    with utils.cwd_src():  # type: ignore
        if not os.path.exists(".env"):
            with open(".env", "w"):
                print(".env file not found, creating an empty one.")

        os.environ["DJANGO_CONFIGURATION"] = "Backoffice"
        with _with_frontend():
            run_server(8000)
