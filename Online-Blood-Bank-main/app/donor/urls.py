from django.urls import path, include

from rest_framework.routers import DefaultRouter

from donor.api import viewset


router = DefaultRouter()
router.register(
    "profile", viewset.DonorProfileViewSet, basename="profile"
)


urlpatterns = [
    path("", include(router.urls)),
]