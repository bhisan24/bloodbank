from django.urls import path, include

from rest_framework.routers import DefaultRouter

from accounts.api import viewset


router = DefaultRouter()
router.register(
    "register-patient", viewset.RegisterPatientView, basename="register-patient",
)
router.register(
    "register-donor", viewset.RegisterDonorView, basename="register-donor"
)
router.register(
    "profile", viewset.UserProfileView, basename="profile"
)
router.register(
    "address", viewset.AddressViewSet, basename="address"
)
router.register(
    "logout", viewset.LogoutAPIView, basename="logout"
)

urlpatterns = [
    path("", include(router.urls)),
    path('forget-password/', viewset.ForgetPasswordView.as_view(), name='forget-password'),
    path('reset-password/', viewset.ResetPasswordView.as_view(), name='reset-password'),
    path("auth/", include('djoser.urls.jwt')),
    path('auth/admin/jwt/refresh/', viewset.CustomRefreshView.as_view(), name='custom_refresh_jwt'),
    path('auth/admin/jwt/create/', viewset.CustomAdminLoginView.as_view(), name='custom_admin_jwt'),
    path('auth/donor/jwt/create/', viewset.CustomDonorLoginView.as_view(), name='custom_donor_jwt'),
    path('auth/patient/jwt/create/', viewset.CustomPatientLoginView.as_view(), name='custom_patient_jwt'),
]