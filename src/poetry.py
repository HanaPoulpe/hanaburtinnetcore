import os
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
    dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(dotenv_file):
        with open(dotenv_file):
            print(".env file not found, creating an empty one.")

    manage.main("poetry-run", "runserver", "0.0.0.0:8000", *sys.argv[1:])


def run_python_tests() -> None:
    subprocess.check_call(["pytest"] + sys.argv[1:])


def build_docker_compose() -> None:
    if r := subprocess.call(("docker-compose", "up", "-d", "--build")):
        exit(r)
    docker_run_migrations()


def stop_docker_compose() -> None:
    if r := subprocess.call(("docker-compose", "down")):
        exit(r)


def start_docker_compose() -> None:
    if r := subprocess.call(("docker-compose", "up")):
        exit(r)


def docker_run_migrations() -> None:
    if r := subprocess.call(
        ("docker-compose", "exec", "backoffice", "python", "src/manage.py", "migrate")
    ):
        exit(r)
