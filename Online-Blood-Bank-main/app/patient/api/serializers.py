from rest_framework import serializers

from patient.models import PatientProfile
from accounts.api.serializers import AddressSerializer

class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializes Patient Profile Object"""
    patient_name = serializers.SerializerMethodField('get_patient_name')
    phone = serializers.SerializerMethodField('get_phone')
    address_detail = serializers.SerializerMethodField('get_address_detail')
    
    def get_address_detail(self, obj):
        if obj.location:
            return AddressSerializer(obj.location).data
        return None
    
    def get_patient_name(self, obj):
        return obj.user.name

    def get_phone(self, obj):
        return obj.user.phone
    
    class Meta:
        model = PatientProfile
        fields = "__all__"
        read_only_fields = ("user",)