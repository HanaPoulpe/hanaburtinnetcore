from queenbees import settings

from . import _mixins as mixins


class Backoffice(settings.Backoffice, mixins.InterfaceAgnostic):
    pass


class Api(settings.Api, mixins.InterfaceAgnostic):
    pass
