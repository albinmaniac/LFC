from lfc_project.validators import validate_image
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models


class FamilyUnit(models.Model):

    family_unit_name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    saint = models.CharField(
        max_length=255,
    )


    saint_photo = models.ImageField(

        upload_to="family_units/photos/",

        blank=True,

        null=True,

        validators=[validate_image],

    )

    president = models.ForeignKey(
        "FamilyMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="president_of_units",
    )

    secretary = models.ForeignKey(
        "FamilyMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="secretary_of_units",
    )


    phone_number = models.CharField(
        max_length=20,
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
        ordering = ["family_unit_name"]
        verbose_name = "Family Unit"
        verbose_name_plural = "Family Units"

    def __str__(self):
        return self.family_unit_name


class Family(models.Model):
    family_unit = models.ForeignKey(
        FamilyUnit,
        on_delete=models.PROTECT,
        related_name="families",
    )

    house_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    address = models.TextField()

    ward_number = models.PositiveIntegerField()


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
        ordering = ["house_name"]
        verbose_name = "Family"
        verbose_name_plural = "Families"
        indexes = [
            models.Index(fields=["family_unit"]),
            models.Index(fields=["ward_number"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.house_name


class FamilyMember(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    class Relationship(models.TextChoices):

        FATHER = "FATHER", "Father (അച്ഛൻ)"

        MOTHER = "MOTHER", "Mother (അമ്മ)"

        HUSBAND = "HUSBAND", "Husband (ഭർത്താവ്)"

        WIFE = "WIFE", "Wife (ഭാര്യ)"

        SON = "SON", "Son (മകൻ)"

        DAUGHTER = "DAUGHTER", "Daughter (മകൾ)"

        BROTHER = "BROTHER", "Brother (സഹോദരൻ)"

        SISTER = "SISTER", "Sister (സഹോദരി)"

        GRANDFATHER = "GRANDFATHER", "Grandfather (മുത്തച്ഛൻ)"

        GRANDMOTHER = "GRANDMOTHER", "Grandmother (മുത്തശ്ശി)"

        GRANDSON = "GRANDSON", "Grandson (കൊച്ചുമകൻ)"

        GRANDDAUGHTER = "GRANDDAUGHTER", "Granddaughter (കൊച്ചുമകൾ)"

        SON_IN_LAW = "SON_IN_LAW", "Son-in-law (മരുമകൻ)"

        DAUGHTER_IN_LAW = "DAUGHTER_IN_LAW", "Daughter-in-law (മരുമകൾ)"

        NEPHEW = "NEPHEW", "Nephew (സഹോദരപുത്രൻ)"

        NIECE = "NIECE", "Niece (സഹോദരപുത്രി)"

        OTHER = "OTHER", "Other (മറ്റുള്ളവർ)"

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name="members",
    )

    first_name = models.CharField(
        max_length=150,
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    baptism_name = models.CharField(
        max_length=255,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    relationship = models.CharField(
        max_length=20,
        choices=Relationship.choices,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to="family_members/photos/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    occupation = models.CharField(
        max_length=255,
        blank=True,
    )

    is_family_head = models.BooleanField(
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
        ordering = ["first_name"]
        verbose_name = "Family Member"
        verbose_name_plural = "Family Members"
        indexes = [
            models.Index(fields=["family"]),
            models.Index(fields=["is_family_head"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def clean(self):

        if not self.is_family_head:
            return

        # Skip validation if the family hasn't been saved yet
        if not self.family or not self.family.pk:
            return

        queryset = FamilyMember.objects.filter(
            family=self.family,
            is_family_head=True,
        )

        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if queryset.exists():
            raise ValidationError(
                "Only one family head is allowed per family."
            )
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        