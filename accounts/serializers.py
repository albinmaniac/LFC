from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from user_agents import parse

from accounts.models import (
    Invitation,
    PasswordResetToken,
    User,
    UserRole,
    UserSession,
    LoginHistory,
)

# Additional model imports
from parish.models import UserPermission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "is_email_verified",
            "last_login",
            "date_joined",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "is_email_verified",
            "last_login",
            "date_joined",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Current password is incorrect."}
            )

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        validate_password(attrs["new_password"], user=user)
        return attrs


# Forgot Password Serializers
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.strip().lower()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        validate_password(attrs["new_password"])

        try:
            reset_token = PasswordResetToken.objects.select_related(
                "user"
            ).get(token=attrs["token"])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(
                {"token": "Invalid reset token."}
            )

        if reset_token.is_used:
            raise serializers.ValidationError(
                {"token": "This reset link has already been used."}
            )

        if reset_token.is_expired:
            raise serializers.ValidationError(
                {"token": "This reset link has expired."}
            )

        attrs["reset_token"] = reset_token
        return attrs


class InvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["email", "role"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        pending_invitation_exists = Invitation.objects.filter(
            email=value,
            status=Invitation.Status.PENDING,
        ).exists()

        if pending_invitation_exists:
            raise serializers.ValidationError(
                "A pending invitation already exists for this email."
            )

        return value

    def validate_role(self, value):
        if value not in UserRole.values:
            raise serializers.ValidationError("Invalid role selected.")

        return value


class InvitationListSerializer(serializers.ModelSerializer):
    invited_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = (
            "id",
            "email",
            "role",
            "status",
            "expires_at",
            "created_at",
            "invited_by_name",
        )
        read_only_fields = fields

    def get_invited_by_name(self, obj):
        if obj.invited_by:
            return obj.invited_by.full_name
        return None


class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": (
                        "Passwords do not match."
                    )
                }
            )

        validate_password(attrs["password"])

        return attrs


# LoginSerializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        attrs["user"] = user
        return attrs


# LoginUserSerializer
class LoginUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
        )
        read_only_fields = fields


# UserSessionSerializer
class UserSessionSerializer(
    serializers.ModelSerializer):

    browser = serializers.SerializerMethodField()
    operating_system = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    user_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:

        model = UserSession

        fields = (
            "id",
            "user_email",
            "user_name",
            "role",
            "session_id",
            "ip_address",
            "user_agent",
            "browser",
            "operating_system",
            "device",
            "last_activity",
            "is_active",
            "created_at",
        )

        read_only_fields = fields

    def get_user_name(self, obj):
        return obj.user.full_name

    def get_browser(self, obj):

        ua = parse(obj.user_agent or "")
        return ua.browser.family

    def get_operating_system(self, obj):

        ua = parse(obj.user_agent or "")
        return ua.os.family

    def get_device(self, obj):

        ua = parse(obj.user_agent or "")

        if ua.is_pc:
            return "Desktop"

        if ua.is_mobile:
            return "Mobile"

        if ua.is_tablet:
            return "Tablet"

        return ua.device.family
    

    def get_role(self, obj):

        return obj.user.role


# LoginHistorySerializer
class LoginHistorySerializer(
    serializers.ModelSerializer):

    browser = serializers.SerializerMethodField()
    operating_system = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    user_email = serializers.EmailField(

        source="user.email",

        read_only=True,

    )

    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):

        return obj.user.full_name

    class Meta:

        model = LoginHistory

        fields = (
            "id",
            "user_email",
            "user_name",
            "ip_address",
            "user_agent",
            "browser",
            "operating_system",
            "device",
            "login_time",
            "logout_time",
            "is_successful",
        )

        read_only_fields = fields

    def get_browser(self, obj):

        ua = parse(obj.user_agent or "")
        return ua.browser.family

    def get_operating_system(self, obj):

        ua = parse(obj.user_agent or "")
        return ua.os.family

    def get_device(self, obj):

        ua = parse(obj.user_agent or "")

        if ua.is_pc:
            return "Desktop"

        if ua.is_mobile:
            return "Mobile"

        if ua.is_tablet:
            return "Tablet"

        return ua.device.family
    
