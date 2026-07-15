# staffs/serializers.py

from rest_framework import serializers

from accounts.models import Invitation
from .models import Staff


class StaffListSerializer(serializers.ModelSerializer):

    photo_url = serializers.SerializerMethodField()
    account_status = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
            "show_email_publicly",
            "show_phone_publicly",
            "designation",
            "photo",
            "photo_url",
            "status",
            "account_status",
            "start_date",
            "end_date",
            "is_active",
        )
        read_only_fields = fields

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

    def get_account_status(self, obj):
        annotated_status = getattr(obj, "invitation_status", None)
        if annotated_status:
            return annotated_status

        if not obj.email:
            return "NOT_INVITED"

        invitation = (
            Invitation.objects.filter(email__iexact=obj.email)
            .order_by("-created_at")
            .first()
        )

        return invitation.status if invitation else "NOT_INVITED"


class StaffDetailSerializer(serializers.ModelSerializer):

    photo_url = serializers.SerializerMethodField()
    account_status = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
            "show_email_publicly",
            "show_phone_publicly",
            "designation",
            "photo",
            "photo_url",
            "account_status",
            "bio",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

    def get_account_status(self, obj):
        annotated_status = getattr(obj, "invitation_status", None)
        if annotated_status:
            return annotated_status

        if not obj.email:
            return "NOT_INVITED"

        invitation = (
            Invitation.objects.filter(email__iexact=obj.email)
            .order_by("-created_at")
            .first()
        )

        return invitation.status if invitation else "NOT_INVITED"


class StaffCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = (
            "name",
            "email",
            "phone_number",
            "show_email_publicly",
            "show_phone_publicly",
            "designation",
            "photo",
            "bio",
            "start_date",
            "end_date",
            "status",
            "is_active",
        )

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Name is required."
            )
        if len(value) < 2:
            raise serializers.ValidationError(
                "Name must contain at least 2 characters."
            )
        return value

    def validate_phone_number(self, value):
        value = value.strip()

        if value and not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise serializers.ValidationError(
                "Enter a valid phone number."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = Staff.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if value and queryset.exists():
            raise serializers.ValidationError(
                "A staff member with this email already exists."
            )

        return value

    def validate_designation(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Designation is required."
            )
        if len(value) < 2:
            raise serializers.ValidationError(
                "Designation must contain at least 2 characters."
            )
        return value
    
    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        if (
            start_date
            and end_date
            and end_date < start_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date cannot be earlier than start date."
                    )
                }
            )

        if attrs.get("email") and not isinstance(
            attrs.get("show_email_publicly", False),
            bool,
        ):
            raise serializers.ValidationError(
                {
                    "show_email_publicly": "Invalid value."
                }
            )

        if attrs.get("phone_number") and not isinstance(
            attrs.get("show_phone_publicly", False),
            bool,
        ):
            raise serializers.ValidationError(
                {
                    "show_phone_publicly": "Invalid value."
                }
            )

        return attrs
