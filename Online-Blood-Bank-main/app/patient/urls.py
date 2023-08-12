from django.urls import path, include

from rest_framework.routers import DefaultRouter

from patient.api import viewset


router = DefaultRouter()
router.register(
    "profile", viewset.PatientProfileViewSet, basename="profile"
)


urlpatterns = [
    path("", include(router.urls)),
]