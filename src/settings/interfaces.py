import pathlib
from pathlib import Path

from django.utils import functional

from . import base


class Backoffice(base.Base):
    INSTALLED_APPS = base.Base.INSTALLED_APPS + [
        "webpack_boilerplate",
    ]

    INTERFACE_DIR = base.Base.BASE_DIR.joinpath("interfaces", "backoffice")

    STATICFILES_DIRS = base.Base.STATICFILES_DIRS + [
        INTERFACE_DIR.joinpath("static_src", "build"),
    ]
    STATIC_ROOT = INTERFACE_DIR.joinpath("static")
    WEBPACK_LOADER = {
        "MANIFEST_FILE": INTERFACE_DIR.joinpath("static_src", "build", "manifest.json"),
    }

    TEMPLATE_DIRS = [INTERFACE_DIR.joinpath("templates")]
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": TEMPLATE_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    ROOT_URLCONF = "interfaces.backoffice.urls"
