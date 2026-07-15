from django.db import models
from lfc_project.validators import validate_image


class Event(models.Model):

    class EventType(models.TextChoices):

        PARISH_FEAST = (
            "PARISH_FEAST",
            "Parish Feast",
        )

        SAINT_DAY_CELEBRATION = (
            "SAINT_DAY_CELEBRATION",
            "Saint Day Celebration",
        )

        HOLY_MASS = (
            "HOLY_MASS",
            "Holy Mass",
        )

        RETREAT = (
            "RETREAT",
            "Retreat",
        )

        CONVENTION = (
            "CONVENTION",
            "Convention",
        )

        PRAYER_MEETING = (
            "PRAYER_MEETING",
            "Prayer Meeting",
        )

        FAMILY_UNIT_MEETING = (
            "FAMILY_UNIT_MEETING",
            "Family Unit Meeting",
        )

        YOUTH_MEETING = (
            "YOUTH_MEETING",
            "Youth Meeting",
        )

        CATECHISM_PROGRAM = (
            "CATECHISM_PROGRAM",
            "Catechism Program",
        )

        NOVENA = (
            "NOVENA",
            "Novena",
        )

        PILGRIMAGE = (
            "PILGRIMAGE",
            "Pilgrimage",
        )

        CHARITY_PROGRAM = (
            "CHARITY_PROGRAM",
            "Charity Program",
        )

        OTHER = (
            "OTHER",
            "Other",
        )

    title = models.CharField(
        max_length=255,
        db_index=True,
    )

    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices,
    )

    family_unit = models.ForeignKey(
        "families.FamilyUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )

    description = models.TextField()

    venue = models.CharField(
        max_length=255,
    )

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    cover_image = models.ImageField(
        upload_to="events/",
        null=True,
        blank=True,
        validators=[validate_image],
    )

    is_public = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-start_datetime",
        ]
        indexes = [
            models.Index(fields=["event_type"]),
            models.Index(fields=["start_datetime"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.title
    
    