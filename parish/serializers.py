from rest_framework import serializers

from accounts.models import User
from .models import (
    Parish,
    MassTiming,
    UserPermission,
)

# MassTiming Serializer
class MassTimingSerializer(serializers.ModelSerializer):

    day_display = serializers.CharField(
        source="get_day_display",
        read_only=True,
    )

    class Meta:
        model = MassTiming
        fields = (
            "id",
            "day",
            "day_display",
            "language",
            "mass_time",
            "description",
            "is_active",
        )


class ParishSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    mass_timings = MassTimingSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Parish

        fields = (
            "id",
            "name",
            "logo",
            "logo_url",
            "cover_image",
            "cover_image_url",
            "address",
            "phone",
            "email",
            "website",
            "diocese",
            "patron_saint",
            "established_year",
            "office_phone",
            "office_email",
            "office_open_time",
            "office_close_time",
            "google_map_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
            "whatsapp_url",
            "history",
            "mission",
            "vision",
            "mass_timings",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def validate_established_year(self, value):
        from datetime import date

        if value is None:
            return value

        current_year = date.today().year

        if value < 1000 or value > current_year:
            raise serializers.ValidationError(
                "Enter a valid established year."
            )

        return value


class ParishUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parish

        fields = (
            "name",
            "logo",
            "cover_image",
            "address",
            "phone",
            "email",
            "website",
            "diocese",
            "patron_saint",
            "established_year",
            "office_phone",
            "office_email",
            "office_open_time",
            "office_close_time",
            "google_map_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
            "whatsapp_url",
            "history",
            "mission",
            "vision",
        )

    def validate_established_year(self, value):
        from datetime import date

        if value is None:
            return value

        current_year = date.today().year

        if value < 1000 or value > current_year:
            raise serializers.ValidationError(
                "Enter a valid established year."
            )

        return value

    def validate(self, attrs):
        open_time = attrs.get("office_open_time")
        close_time = attrs.get("office_close_time")

        if (
            open_time
            and close_time
            and open_time >= close_time
        ):
            raise serializers.ValidationError(
                {
                    "office_close_time": (
                        "Office closing time must be later than opening time."
                    )
                }
            )

        return attrs


class UserPermissionSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    permission_display = serializers.CharField(
        source="get_permission_display",
        read_only=True,
    )

    class Meta:
        model = UserPermission

        fields = (
            "id",
            "user",
            "user_email",
            "permission",
            "permission_display",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )


class AssignPermissionSerializer(
        serializers.ModelSerializer
    ):

    class Meta:
        model = UserPermission

        fields = (
            "user",
            "permission",
        )

    def validate_user(self, value):

        if value.role == "SUPERADMIN":
            raise serializers.ValidationError(
                "SuperAdmin already has all permissions."
            )

        return value

    def validate(self, attrs):

        user = attrs.get("user")
        permission = attrs.get("permission")

        if UserPermission.objects.filter(
            user=user,
            permission=permission,
        ).exists():
            raise serializers.ValidationError(
                {
                    "permission": (
                        "This permission is already assigned to the user."
                    )
                }
            )

        return attrs


class UserPermissionBulkSerializer(
        serializers.Serializer
    ):

    user_id = serializers.IntegerField()

    permissions = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
    )

    def validate_user_id(self, value):
        try:
            user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User not found."
            )
        if user.role == "SUPERADMIN":
            raise serializers.ValidationError(
                "SuperAdmin does not require permissions."
            )
        return value

    def validate_permissions(self, value):
        valid_permissions = {
            choice[0]
            for choice in UserPermission.PermissionChoices.choices
        }

        invalid_permissions = [
            permission
            for permission in value
            if permission not in valid_permissions
        ]

        if invalid_permissions:
            raise serializers.ValidationError(
                f"Invalid permissions: {', '.join(invalid_permissions)}"
            )

        return list(dict.fromkeys(value))