from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.db.models import Sum

from blood_bank.api import serializers
from blood_bank import models
from core.infrastructure.check_permissions import BloodStockPermissions, BloodRequestPermissions, IsTokenValid


class BloodDonationViewSet(viewsets.ModelViewSet):
    """API Views for Handling Blood Donation Profile in the System"""
    
    serializer_class = serializers.BloodDonationSerializer
    permission_classes = (IsAuthenticated, BloodStockPermissions, IsTokenValid)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.BloodStock.objects.all()
        return models.BloodStock.objects.filter(donor=self.request.user.donor_profile)
    
    def perform_create(self, serializer):
        serializer.save(donor=self.request.user.donor_profile,blood_group=self.request.user.donor_profile.blood_group)


class BloodRequestViewSet(viewsets.ModelViewSet):
    """API Views for Handling Blood Request in the System"""
    
    queryset = models.BloodRequest.objects.all()
    serializer_class = serializers.BloodRequestSerializer
    permission_classes = (IsAuthenticated, BloodRequestPermissions, IsTokenValid)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.BloodRequest.objects.all()
        return models.BloodRequest.objects.filter(patient=self.request.user.patient_profile)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)


class BloodRequestStatusViewSet(viewsets.ModelViewSet):
    """API Views for Handling Blood Request Status By Adminin the System"""
    
    queryset = models.BloodRequest.objects.all()
    serializer_class = serializers.BloodRequestStatusSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, IsTokenValid)
    http_method_names = ["get","patch"]


class BloodDonationStatusViewSet(viewsets.ModelViewSet):
    """API Views for Handling Blood Donation Status By Adminin the System"""
    
    queryset = models.BloodStock.objects.all()
    serializer_class = serializers.BloodDonationStatusSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, IsTokenValid)
    http_method_names = ["get","patch"]


class AvailableBloodStockView(APIView):
    """API View for Handling ALl Available Blood Stocks in the System"""
    
    permission_classes = (IsAuthenticated, IsTokenValid)
    
    def get(self, request, format=None):
        data = {
            "a_positive": models.BloodStock.objects.filter(blood_group="A+",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "a_negative": models.BloodStock.objects.filter(blood_group="A-",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "b_positive": models.BloodStock.objects.filter(blood_group="B+",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "b_negative": models.BloodStock.objects.filter(blood_group="B-",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "ab_positive": models.BloodStock.objects.filter(blood_group="AB+",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "ab_negative": models.BloodStock.objects.filter(blood_group="AB-",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "o_positive": models.BloodStock.objects.filter(blood_group="O+",status="PENDING").aggregate(Sum('quantity'))['quantity__sum'],
            "o_negative": models.BloodStock.objects.filter(blood_group="O-",status="PENDING").aggregate(Sum('quantity'))['quantity__sum']
        }
        return Response(data, status=status.HTTP_200_OK)