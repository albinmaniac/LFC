from django.apps import AppConfig


class ParishConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "parish"

    def ready(self):
        from parish.models import Parish
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(
            Parish,
            ["logo", "cover_image"],
        )
