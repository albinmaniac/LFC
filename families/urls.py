from django.urls import path

from .views import (

    FamilyListCreateAPIView,

    FamilyMemberListCreateAPIView,

    FamilyMemberRetrieveUpdateDestroyAPIView,

    FamilyRetrieveUpdateDestroyAPIView,

    FamilyUnitListCreateAPIView,

    FamilyUnitRetrieveUpdateDestroyAPIView,

)

app_name = "families"

urlpatterns = [

    # Family Units

    path("family-units/",FamilyUnitListCreateAPIView.as_view(),name="family-unit-list-create",),

    path("family-units/<int:pk>/",FamilyUnitRetrieveUpdateDestroyAPIView.as_view(),name="family-unit-detail",),

    # Families

    path("families/",FamilyListCreateAPIView.as_view(),name="family-list-create",),

    path("families/<int:pk>/",FamilyRetrieveUpdateDestroyAPIView.as_view(),name="family-detail",),

    # Family Members

    path("family-members/",FamilyMemberListCreateAPIView.as_view(),name="family-member-list-create",),

    path("family-members/<int:pk>/",FamilyMemberRetrieveUpdateDestroyAPIView.as_view(),name="family-member-detail",),

]