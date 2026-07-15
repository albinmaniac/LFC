from django.db import models

from lfc_project.validators import validate_image
from families.models import FamilyMember


class GroupRole(models.TextChoices):

    PRESIDENT = "PRESIDENT", "President"

    SECRETARY = "SECRETARY", "Secretary"

    TREASURER = "TREASURER", "Treasurer"

    COORDINATOR = "COORDINATOR", "Coordinator"

    LEADER = "LEADER", "Leader"

    MEMBER = "MEMBER", "Member"


class ParishGroup(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    patron_saint = models.CharField(
        max_length=255,
        blank=True,
    )

    photo = models.ImageField(
        upload_to="parish_groups/photos/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    leader = models.ForeignKey(
        FamilyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_groups",
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
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
        ordering = ["name"]

    def __str__(self):
        return self.name


class ParishGroupMember(models.Model):

    group = models.ForeignKey(
        ParishGroup,
        on_delete=models.CASCADE,
        related_name="members",
    )

    member = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name="parish_groups",
    )


    role = models.CharField(
        max_length=20,
        choices=GroupRole.choices,
        default=GroupRole.MEMBER,
    )

    joined_date = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "group",
            "member",
        )
        ordering = [
            "group",
            "member__first_name",
        ]

    def __str__(self):
        return f"{self.member} - {self.group}"
