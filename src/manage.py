#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from typing import Any

import dotenv


def _dotenv() -> None:
    env_suffix = os.environ.get("DJANGO_CONFIGURATION", "")
    env_base_path = os.environ.get("ENV_FILE", os.path.join(os.path.dirname(__file__), ".env"))

    env_paths = [
        ".".join(
            [
                env_base_path,
                env_suffix,
            ]
        ),
        env_base_path,
    ]
    for env_path in env_paths:
        if os.path.isfile(env_path) or os.path.islink(env_path):
            dotenv.load_dotenv(env_path)


def main(*argv: Any) -> None:
    """Run administrative tasks."""
    _dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "queenbees.settings")
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(argv or sys.argv)  # type: ignore


if __name__ == "__main__":
    main()
