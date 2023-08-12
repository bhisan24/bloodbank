from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from patient.api import serializers
from patient import models
from core.infrastructure.check_permissions import PatientProfilePermissions, IsTokenValid


class PatientProfileViewSet(viewsets.ModelViewSet):
    """API Views for Handling Patient Profile in the System"""
    
    serializer_class = serializers.PatientProfileSerializer
    permission_classes = (IsAuthenticated, PatientProfilePermissions, IsTokenValid)
    http_method_names = ["get","put","patch"]
    
    def get_queryset(self):
        return models.PatientProfile.objects.filter(user=self.request.user)