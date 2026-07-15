from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self):
        from events.models import Event
        from lfc_project.signals.cloudinary_cleanup import (
            register_cloudinary_cleanup,
        )

        register_cloudinary_cleanup(Event, "cover_image")
