import contextlib
import multiprocessing
import os
import signal
import subprocess
import sys
from typing import Any, Generator

import manage


@contextlib.contextmanager
def _until_terminated() -> Generator[None, None, None]:
    class Signal(RuntimeError):
        pass

    def _signal_handler(signum: int, frame: Any) -> None:
        raise Signal()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    try:
        yield
    except Signal:
        pass
    signal.signal(signal.SIGINT, None)
    signal.signal(signal.SIGTERM, None)


_CWD = os.path.dirname(__file__)


def run_isort() -> None:
    subprocess.check_call(["isort"] + (sys.argv[1:] or ["."]))


def run_black() -> None:
    subprocess.check_call(["black"] + (sys.argv[1:] or ["."]))


def run_mypy() -> None:
    subprocess.check_call(["mypy"] + (sys.argv[1:] or ["."]))


def run_eslint() -> None:
    eslint_bin = ["npm", "run", "eslint"]
    subprocess.check_call(
        eslint_bin + (sys.argv[1:]),
        cwd=_CWD,
    )


def run_js_tests() -> None:
    subprocess.check_call(["npm", "test"] + sys.argv[1:])


def run_linters() -> None:
    errors: list[Exception] = []
    for name, check in (("isort", run_isort), ("black", run_black)):
        print("Running %s..." % name)
        try:
            check()
        except subprocess.CalledProcessError as err:
            errors.append(err)

    if errors:
        raise ExceptionGroup("Linter failed", errors)


def run_backoffice_server() -> None:
    dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(dotenv_file):
        with open(dotenv_file):
            print(".env file not found, creating an empty one.")

    webpack = multiprocessing.Process(
        target=build_frontend, kwargs={"set_watcher_mode": True}, name="webpack"
    )
    with _until_terminated():
        webpack.start()
        run_server()

    if webpack.is_alive():
        webpack.terminate()
        webpack.join()


def run_server() -> None:
    manage.main("poetry-run", "runserver", "0.0.0.0:8000", *sys.argv[1:])


def run_python_tests() -> None:
    subprocess.check_call(["pytest"] + sys.argv[1:])


def build_docker_compose() -> None:
    subprocess.run(("docker-compose", "up", "-d", "--build"))
    docker_run_migrations()


def stop_docker_compose() -> None:
    subprocess.run(("docker-compose", "down"))


def start_docker_compose() -> None:
    subprocess.run(("docker-compose", "up"))


def docker_run_migrations() -> None:
    subprocess.run(("docker-compose", "exec", "backoffice", "python", "src/manage.py", "migrate"))


def build_frontend(set_watcher_mode: bool = False) -> None:
    watcher = "start" if set_watcher_mode else "watch"
    subprocess.run(
        ("npm", "run", watcher),
        cwd=os.path.join(_CWD, "interfaces/backoffice/static_src"),
    )


def install_frontend_requirements() -> None:
    os.chdir(os.path.dirname(__file__) + "/interfaces/backoffice/static_src")

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
        subprocess.run(installer)


def create_superuser() -> None:
    manage.main("poetry-run", "createsuperuser")
