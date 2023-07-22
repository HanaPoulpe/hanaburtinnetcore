import os
from typing import Type

from configurations.importer import install
from mypy.version import __version__
from mypy_django_plugin import main


def plugin(version: str) -> Type[main.NewSemanalDjangoPlugin]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Base")
    install()
    return main.plugin(version)
