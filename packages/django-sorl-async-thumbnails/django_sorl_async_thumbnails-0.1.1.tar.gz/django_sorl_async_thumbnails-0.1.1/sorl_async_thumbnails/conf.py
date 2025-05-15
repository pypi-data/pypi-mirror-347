
from django.conf import settings as django_settings
from . import defaults 

class AsyncThumbnailSettings:
    """
    Settings proxy that will lookup first in the django settings, and then in the conf
    defaults.
    """
    def __getattr__(self, name):
        if name != name.upper():
            raise AttributeError(name)
        try:
            return getattr(django_settings, name)
        except AttributeError:
            return getattr(defaults, name)
        

settings = AsyncThumbnailSettings()