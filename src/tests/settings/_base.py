import uuid

from queenbees import settings
from queenbees.utils import environ


class BaseTest(settings.Base):
    SECRET_KEY = environ.get_str("DJANGO_SECRET_KEY", uuid.getnode().to_bytes(16, "big").hex())


class UnitTest(BaseTest):
    pass
