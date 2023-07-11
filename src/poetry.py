import subprocess
import sys

import manage


def run_isort() -> None:
    if r := subprocess.call(["isort"] + (sys.argv[1:] or ["."])):
        exit(r)


def run_black() -> None:
    if r := subprocess.call(["black"] + (sys.argv[1:] or ["."])):
        exit(r)


def run_mypy() -> None:
    if r := subprocess.call(["mypy"] + (sys.argv[1:] or ["."])):
        exit(r)


def run_linters() -> None:
    print("Running isort...")
    run_isort()
    print("Running black...")
    run_black()


def run_backoffice_server() -> None:
    manage.main("poetry-run", "runserver", "8000", *sys.argv[1:])


def run_python_tests() -> None:
    subprocess.check_call(["pytest"] + sys.argv[1:])
