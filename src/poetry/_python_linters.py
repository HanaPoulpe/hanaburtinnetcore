import os
import subprocess
import sys

from . import _utils as utils


@utils.sub_command_wrapper
def run_isort() -> None:
    subprocess.check_call(["isort"] + (sys.argv[1:] or [utils.SRC_DIR]), cwd=utils.PROJECT_DIR)


@utils.sub_command_wrapper
def run_black() -> None:
    subprocess.check_call(["black"] + (sys.argv[1:] or [utils.SRC_DIR]), cwd=utils.PROJECT_DIR)


@utils.sub_command_wrapper
def run_mypy() -> None:
    os.environ["DJANGO_CONFIGURATION"] = "Base"
    subprocess.check_call(["mypy"] + (sys.argv[1:] or [utils.SRC_DIR]), cwd=utils.PROJECT_DIR)


@utils.sub_command_wrapper
def run_import_linter() -> None:
    subprocess.check_call(["lint-imports"], cwd=utils.PROJECT_DIR)


def run_linters() -> None:
    linters = (
        ("isort", run_isort),
        ("black", run_black),
        ("mypy", run_mypy),
        ("import-linter", run_import_linter),
    )

    errors: list[Exception] = []
    for name, check in linters:
        print(f"Running linter {name}")
        try:
            check()
        except subprocess.CalledProcessError as err:
            errors.append(err)

    if errors:
        raise ExceptionGroup("Linter failed:", errors)
