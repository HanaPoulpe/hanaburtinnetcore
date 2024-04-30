import uuid

from queenbees import settings
from queenbees.utils import environ


class BaseTest(settings.Base):
    BACKOFFICE_URL = environ.get_str("BACKOFFICE_URL", "backoffice.url")
    API_URL = environ.get_str("API_URL", "api.url")

    SECRET_KEY = environ.get_str("DJANGO_SECRET_KEY", uuid.getnode().to_bytes(16, "big").hex())


class UnitTest(BaseTest):
    pass
