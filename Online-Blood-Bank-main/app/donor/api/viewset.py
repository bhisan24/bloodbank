from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from donor.api import serializers
from donor import models
from core.infrastructure.check_permissions import DonorProfilePermissions, IsTokenValid


class DonorProfileViewSet(viewsets.ModelViewSet):
    """API Views for Handling Donor Profile in the System"""
    
    serializer_class = serializers.DonorProfileSerializer
    permission_classes = (IsAuthenticated, DonorProfilePermissions, IsTokenValid)
    http_method_names = ["get","put","patch"]
    
    def get_queryset(self):
        return models.DonorProfile.objects.filter(user=self.request.user)