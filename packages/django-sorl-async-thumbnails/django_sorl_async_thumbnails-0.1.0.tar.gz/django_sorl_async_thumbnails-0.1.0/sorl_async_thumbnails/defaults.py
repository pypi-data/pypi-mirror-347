from django.conf import settings
from sorl.thumbnail.helpers import get_module_class


ASYNC_THUMBNAILS_BY_DEFAULT = False
ASYNC_THUMBNAILS_PLACEHOLDER = False
ASYNC_THUMBNAILS_GENETARE_PLACEHOLDER_THUMB = False
ASYNC_THUMBNAILS_PLACEHOLDER_STATICFILE = '/async_thumbnails/processing_placeholder.jpg'

ASYNC_THUMBNAILS_STATICFILES_STORAGE = get_module_class(settings.STORAGES.get('staticfiles').get('BACKEND'))()