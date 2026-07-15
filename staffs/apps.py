from django.apps import AppConfig


class StaffsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staffs"

    def ready(self):
        from staffs.models import Staff
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(Staff, "photo")
