from django.urls import path

from parish.views import *

app_name = "parish"

urlpatterns = [

    path("",ParishDetailAPIView.as_view(),name="parish-detail",),
    path("manage/",ParishUpdateAPIView.as_view(),name="parish-update",),

    # Mass Timings
    path(
        "mass-timings/",
        MassTimingListCreateAPIView.as_view(),
        name="mass-timing-list-create",
    ),

    path(
        "mass-timings/<int:pk>/",
        MassTimingRetrieveUpdateDestroyAPIView.as_view(),
        name="mass-timing-detail",
    ),



    #dashboard
    path("dashboard/",DashboardAPIView.as_view(),name="dashboard",),

    # Permissions
    path(
        "permissions/",
        PermissionListCreateAPIView.as_view(),
        name="permission-list-create",
    ),

    path(
        "permissions/<int:pk>/",
        UserPermissionDeleteAPIView.as_view(),
        name="permission-delete",
    ),

    path(
        "permissions/user/<int:user_id>/",
        UserPermissionsAPIView.as_view(),
        name="user-permissions",
    ),

    path(
        "permissions/bulk/",
        UserPermissionBulkUpdateAPIView.as_view(),
        name="permission-bulk-update",
    ),
]