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

    def _signal_handler(signum: int, frame: Any):
        raise Signal()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    try:
        yield
    except Signal:
        pass
    signal.signal(signal.SIGINT, None)
    signal.signal(signal.SIGTERM, None)


def run_isort() -> None:
    subprocess.run(["isort"] + (sys.argv[1:] or ["."]))


def run_black() -> None:
    subprocess.run(["black"] + (sys.argv[1:] or ["."]))


def run_mypy() -> None:
    subprocess.run(["mypy"] + (sys.argv[1:] or ["."]))


def run_linters() -> None:
    print("Running isort...")
    run_isort()
    print("Running black...")
    run_black()


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
    os.chdir(os.path.dirname(__file__))
    watcher = ("--watch",) if set_watcher_mode else tuple()
    subprocess.run(("npx", "webpack", "--config", "./backoffice/webpack.config.js", *watcher))


def install_frontend_requirements() -> None:
    dependencies = (("npn", "install"),)

    for installer in dependencies:
        subprocess.run(installer)
