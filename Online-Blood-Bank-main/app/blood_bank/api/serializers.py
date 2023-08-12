from rest_framework import serializers

from blood_bank import models
from donor.api.serializers import DonorProfileSerializer
from patient.api.serializers import PatientProfileSerializer


class BloodDonationSerializer(serializers.ModelSerializer):
    """Serializes Blood Stock Object"""

    donor_detail = serializers.SerializerMethodField('get_donor_detail')
    
    def get_donor_detail(self, obj):
        return DonorProfileSerializer(obj.donor).data
    
    class Meta:
        model = models.BloodStock
        fields = [
            "id",
            "blood_group",
            "quantity",
            "donor_detail",
            "status"
        ]
        read_only_fields = ('id','blood_group', 'donor_detail', 'status')


class BloodRequestSerializer(serializers.ModelSerializer):
    """Serializes Blood Request Object"""
    
    patient_detail = serializers.SerializerMethodField('get_patient_detail')
    
    def get_patient_detail(self, obj):
        return PatientProfileSerializer(obj.patient).data
    
    class Meta:
        model = models.BloodRequest
        fields = [
            "id",
            "blood_group",
            "quantity",
            "patient_detail",
            "status"
        ]
        read_only_fields = ('id','patient_detail','status')


class BloodRequestStatusSerializer(serializers.ModelSerializer):
    """Serializes Blood Request Object"""
    
    patient_detail = serializers.SerializerMethodField('get_patient_detail')
    
    def get_patient_detail(self, obj):
        return PatientProfileSerializer(obj.patient).data
    
    class Meta:
        model = models.BloodRequest
        fields = [
            "id",
            "blood_group",
            "quantity",
            "patient_detail",
            "status"
        ]
        read_only_fields = ('id','blood_group','quantity','patient_detail')
    
    def validate(self, attrs):
        status = attrs.get("status")
        instance = getattr(self, 'instance', None)
        if status == None:
            raise serializers.ValidationError("STATUS IS REQUIRED")
        if instance.status == "DELIVERY COMPLETED":
            raise serializers.ValidationError("REQUEST ALREADY COMPLETED CANNOT CHANGE STATUS")
        return super().validate(attrs)


class BloodDonationStatusSerializer(serializers.ModelSerializer):
    """Serializes Blood Stock Object"""
    
    donor_detail = serializers.SerializerMethodField('get_donor_detail')
    
    def get_donor_detail(self, obj):
        return DonorProfileSerializer(obj.donor).data
    
    class Meta:
        model = models.BloodStock
        fields = [
            "id",
            "blood_group",
            "quantity",
            "donor_detail",
            "status"
        ]
        read_only_fields = ('id','blood_group','quantity','donor_detail')
    
    def validate(self, attrs):
        status = attrs.get("status")
        instance = getattr(self, 'instance', None)
        if status == None:
            raise serializers.ValidationError("STATUS IS REQUIRED")
        if instance.status == "DELIVERY COMPLETED":
            raise serializers.ValidationError("REQUEST ALREADY COMPLETED CANNOT CHANGE STATUS")
        return super().validate(attrs)