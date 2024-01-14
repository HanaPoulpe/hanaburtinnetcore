import os
import sys

import manage

from . import _utils as utils


def run_server(port: int = 8000) -> None:
    manage.main("poetry-run", "runserver", f"0.0.0.0:{port}", *sys.argv[1:])


def run_backoffice_server() -> None:
    with utils.cwd_src():  # type: ignore
        if not os.path.exists(".env"):
            with open(".env", "w"):
                print(".env file not found, creating an empty one.")

        os.environ["DJANGO_CONFIGURATION"] = "Backoffice"
        run_server(8000)
