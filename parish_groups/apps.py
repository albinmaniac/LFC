from django.apps import AppConfig


class ParishGroupsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "parish_groups"

    def ready(self):
        from parish_groups.models import ParishGroup
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(ParishGroup, "photo")