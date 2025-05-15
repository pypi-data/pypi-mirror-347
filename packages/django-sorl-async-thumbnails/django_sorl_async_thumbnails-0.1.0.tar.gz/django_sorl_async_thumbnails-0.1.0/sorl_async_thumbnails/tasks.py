from celery import shared_task
from sorl.thumbnail import default
from sorl.thumbnail.images import ImageFile
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.conf import settings
import logging
logger = logging.getLogger(__name__)


@shared_task
def create_thumbnail(file_, geometry_string, options):
    _thumb_created = None
    _result = {}
    _reason = None
    thumbnail = ImageFile(file_, default.storage)

    if settings.THUMBNAIL_FORCE_OVERWRITE or not thumbnail.exists():
        source = ImageFile(file_)
        thumb = get_thumbnail(source, geometry_string, create_async=False, **options)

        if thumb:
            _thumb_created = True
            _reason = 'created'
            _result = {
                'key': thumb.key,
                'url': thumb.url,
            }

    else:
       _thumb_created=False
       _reason='already_exists'
       logger.info('Thumbnail already exists')

    return {
        "created": _thumb_created,
        "result": _result,
        "reason": _reason
    }