import uuid

from queenbees import settings
from queenbees.utils import environ


class Base(settings.Base):
    DEBUG = True
    SECRET_KEY = environ.get_str("DJANGO_SECRET_KEY", uuid.getnode().to_bytes(16, "big").hex())
