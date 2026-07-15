from django.apps import AppConfig
class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'

    def ready(self):
        from gallery.models import Album, Photo
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(Album, "cover_image")
        register_cloudinary_cleanup(Photo, "image")