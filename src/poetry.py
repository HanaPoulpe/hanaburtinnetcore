import subprocess


def run_isort(files: list[str] | None = None) -> None:
    if r := subprocess.call(['isort'] + (files or ['.'])):
        exit(r)


def run_black(files: list[str] | None = None) -> None:
    if r := subprocess.call(['black'] + (files or ['.'])):
        exit(r)


def run_mypy(files: list[str] | None = None) -> None:
    if r := subprocess.call(['mypy'] + (files or ['.'])):
        exit(r)


def run_linters(files: list[str] | None = None) -> None:
    print('Running isort...')
    run_isort(files)
    print('Running black...')
    run_black(files)
