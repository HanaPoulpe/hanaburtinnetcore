import subprocess
from collections.abc import Sequence


def run_isort(files: Sequence[str] | None = None) -> None:
    if r := subprocess.call(["isort"] + (files or ["."])):
        exit(r)


def run_black(files: Sequence[str] | None = None) -> None:
    if r := subprocess.call(["black"] + (files or ["."])):
        exit(r)


def run_linters(files: Sequence[str] | None = None) -> None:
    print("Running isort...")
    run_isort(files)
    print("Running black...")
    run_black(files)
