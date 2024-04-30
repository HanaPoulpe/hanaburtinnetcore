import uuid

from queenbees import settings
from queenbees.utils import environ


class Base(settings.Base):
    BACKOFFICE_URL = environ.get_str("BACKOFFICE_URL", "localhost:8000")
    API_URL = environ.get_str("API_URL", "localhost:8001")

    DEBUG = True
    SECRET_KEY = environ.get_str("DJANGO_SECRET_KEY", uuid.getnode().to_bytes(16, "big").hex())
