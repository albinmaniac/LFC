from django.apps import AppConfig


class NoticesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notices"

    def ready(self):
        from notices.models import Notice
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(Notice, "attachment")
