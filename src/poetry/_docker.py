import subprocess

from . import _utils as utils


@utils.sub_command_wrapper
def build_docker_compose() -> None:
    subprocess.run(("docker-compose", "up", "-d", "--build"))
    docker_run_migrations()


@utils.sub_command_wrapper
def stop_docker_compose() -> None:
    subprocess.run(("docker-compose", "down"))


@utils.sub_command_wrapper
def start_docker_compose() -> None:
    subprocess.run(("docker-compose", "up"))


@utils.sub_command_wrapper
def docker_run_migrations() -> None:
    subprocess.run(("docker-compose", "exec", "backoffice", "python", "src/manage.py", "migrate"))
