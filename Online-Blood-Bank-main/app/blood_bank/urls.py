from django.urls import path, include

from rest_framework.routers import DefaultRouter

from blood_bank.api import viewset


router = DefaultRouter()
router.register(
    "donate-blood", viewset.BloodDonationViewSet, basename="donate-blood"
)
router.register(
    "blood-request", viewset.BloodRequestViewSet, basename="blood-request"
)
router.register(
    "request-status", viewset.BloodRequestStatusViewSet, basename="request-status"
)
router.register(
    "donation-status", viewset.BloodDonationStatusViewSet, basename="donation-status"
)

urlpatterns = [
    path("", include(router.urls)),
    path("blood-stock/", viewset.AvailableBloodStockView.as_view(), name='stock'),
]