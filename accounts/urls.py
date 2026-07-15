from django.urls import include, path
from accounts.views import (

    AcceptInvitationAPIView,
    LoginAPIView,
    CurrentUserAPIView,
    ChangePasswordAPIView,
    PasswordResetUserListAPIView,
    SendPasswordResetAPIView,
    ResetPasswordAPIView,
    InvitationCreateAPIView,
    CancelInvitationAPIView,
    ResendInvitationAPIView,
    InvitationDestroyAPIView,

    ActiveSessionListAPIView,
    LoginHistoryListAPIView,

    LogoutAPIView,
    LogoutAllDevicesAPIView,
    ForceLogoutAPIView,

)

urlpatterns = [

    path("login/",LoginAPIView.as_view(),name="login",),

    path("me/",CurrentUserAPIView.as_view(),name="current-user",),


    path(
    "users/",
    PasswordResetUserListAPIView.as_view(),
    name="password-reset-user-list",
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),

    path(
        "users/<int:user_id>/send-password-reset/",
        SendPasswordResetAPIView.as_view(),
        name="send-password-reset",
    ),

    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),

    path("invitations/",InvitationCreateAPIView.as_view(),name="create-invitation",),

    path(
        "invitations/<int:pk>/cancel/",
        CancelInvitationAPIView.as_view(),
        name="cancel-invitation",
    ),

    path(
        "invitations/<int:pk>/resend/",
        ResendInvitationAPIView.as_view(),
        name="resend-invitation",
    ),

    path(
        "invitations/<int:pk>/",
        InvitationDestroyAPIView.as_view(),
        name="delete-invitation",
    ),

    path("accept-invitation/",AcceptInvitationAPIView.as_view(),name="accept-invitation",),

    # Settings / Security

    path("settings/sessions/",ActiveSessionListAPIView.as_view(),name="active-sessions",),

    path("settings/login-history/",LoginHistoryListAPIView.as_view(),name="login-history",),

    path("settings/logout/",LogoutAPIView.as_view(),name="logout",),

    path("settings/logout-all/",LogoutAllDevicesAPIView.as_view(),name="logout-all",),

    path("settings/sessions/<int:pk>/force-logout/",ForceLogoutAPIView.as_view(),name="force-logout",),

]
