from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserSession


class SessionJWTAuthentication(JWTAuthentication):
    """
    JWT authentication integrated with the application's session tracking.

    Responsibilities:
    - Validate the JWT using SimpleJWT.
    - Ensure the corresponding UserSession is still active.
    - Validate the session token version.
    - Update last_activity on every authenticated request.
    """

    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, validated_token = result

        session_id = validated_token.get("session_id")
        token_version = validated_token.get("token_version")

        if not session_id:
            raise AuthenticationFailed(
                "Invalid authentication session."
            )

        session = (
            UserSession.objects.select_related("user")
            .filter(
                session_id=session_id,
                user=user,
                is_active=True,
            )
            .first()
        )

        if session is None:
            raise AuthenticationFailed(
                "Session expired or signed out."
            )

        if (
            token_version is not None
            and token_version != session.token_version
        ):
            raise AuthenticationFailed(
                "Session has been invalidated."
            )

        session.last_activity = timezone.now()
        session.save(update_fields=["last_activity"])

        return user, validated_token