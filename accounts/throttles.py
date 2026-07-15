from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class PasswordResetRateThrottle(AnonRateThrottle):
    scope = "password_reset"


class InvitationRateThrottle(UserRateThrottle):
    scope = "invitation"

    def get_throttles(self):
        if self.request.method == "POST":
            return [InvitationRateThrottle()]
        return []


class RefreshTokenRateThrottle(UserRateThrottle):
    scope = "refresh_token"