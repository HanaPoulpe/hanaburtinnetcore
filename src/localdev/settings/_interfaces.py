from queenbees import settings

from . import _base as base


class Backoffice(settings.Backoffice, base.Base):
    pass


class Api(settings.Api, base.Base):
    pass
