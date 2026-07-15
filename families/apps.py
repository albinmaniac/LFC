from django.apps import AppConfig


class FamiliesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "families"

    def ready(self):
        from families.models import FamilyUnit, FamilyMember
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(FamilyUnit, "saint_photo")
        register_cloudinary_cleanup(FamilyMember, "photo")
