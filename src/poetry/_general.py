import os
import subprocess
import sys

import manage

from . import _utils as utils


@utils.sub_command_wrapper
def build_frontend(set_watcher_mode: bool = False) -> None:
    watcher = "build" if set_watcher_mode else "watch"
    subprocess.run(
        ("npm", "run", watcher),
        cwd=os.path.join(utils.SRC_DIR, "queenbees/interfaces/backoffice/static_src"),
    )


@utils.sub_command_wrapper
def install_frontend_requirements() -> None:
    match sys.argv:
        case [_]:
            dependencies = [["npm", "install", "--omit", "dev"]]
        case [_, "--test"]:
            dependencies = [["npm", "install"]]
        case _:
            print("install-frontend-requirements: installs requirements to run the application.")
            print("install-frontend-requirements --test: install tests requirements.")
            raise RuntimeError("Unknown frontend installation parameters.")

    for installer in dependencies:
        subprocess.run(
            installer,
            cwd=os.path.join(utils.SRC_DIR, "queenbees/interfaces/backoffice/static_src"),
        )


def create_superuser() -> None:
    manage.main("poetry-run", "createsuperuser")
