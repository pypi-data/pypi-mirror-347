from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail import default
from sorl.thumbnail.images import ImageFile
from .conf import settings as at_settings
from sorl.thumbnail.conf import settings, defaults as default_settings
from .tasks import create_thumbnail

class AsyncImageFile(ImageFile):
    is_available = False

    


class AsyncThumbnailBackend(ThumbnailBackend):
    def get_thumbnail(self, file_, geometry_string, **options):
            
        _generate_async=False
        if at_settings.ASYNC_THUMBNAILS_BY_DEFAULT == True:
            _generate_async=True

        if str(options.get('create_async', '')).lower() == 'true':
            _generate_async = True
        elif str(options.get('create_async', '')).lower() == 'false':
            _generate_async = False

        options.pop('create_async', None)

        source = AsyncImageFile(file_)

        # preserve image filetype
        if settings.THUMBNAIL_PRESERVE_FORMAT:
            options.setdefault('format', self._get_format(source))

        for key, value in self.default_options.items():
            options.setdefault(key, value)

        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames being generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)

        # If generating thumbnail not in async mode
        if _generate_async == False:
            t = super().get_thumbnail(source, geometry_string, **options)
            return t

        name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = AsyncImageFile(name, default.storage)
        cached = default.kvstore.get(thumbnail)

        if cached:
            cached_wrapped = cached
            # TODO: Переделать
            cached_wrapped.__class__ = AsyncImageFile
            cached_wrapped.is_available = True
            return cached_wrapped
        
        # Return placeholder
        if at_settings.ASYNC_THUMBNAILS_PLACEHOLDER:
            static_storage=at_settings.ASYNC_THUMBNAILS_STATICFILES_STORAGE
            placeholder_image = AsyncImageFile(static_storage.location + at_settings.ASYNC_THUMBNAILS_PLACEHOLDER_STATICFILE, 
                                          storage=static_storage)
            
            if at_settings.ASYNC_THUMBNAILS_GENERATE_PLACEHOLDER_THUMB:
                # Not the best solution as it generates a GET request to the storage, 
                # but unfortunately sorl.thumbnail doesn't allow you to 
                # create thumbnails from static files.

                thumbnail_placeholder = super().get_thumbnail(placeholder_image, geometry_string, **options)
                thumbnail_placeholder_wrapped = AsyncImageFile(thumbnail_placeholder)

                thumbnail=thumbnail_placeholder_wrapped
            else:
                thumbnail=placeholder_image

        else:
            thumbnail.name = file_.name
            

        # Start async thumbnail generation task
        job = create_thumbnail.delay(file_.name, geometry_string, options)
        return thumbnail