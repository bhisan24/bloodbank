from rest_framework import serializers

from donor.models import DonorProfile
from accounts.api.serializers import AddressSerializer


class DonorProfileSerializer(serializers.ModelSerializer):
    """Serializes Donor Profile Object"""

    address_detail = serializers.SerializerMethodField('get_address_detail')
    donor_name = serializers.SerializerMethodField('get_donor_name')
    phone = serializers.SerializerMethodField('get_phone')
    
    def get_address_detail(self, obj):
        if obj.location:
            return AddressSerializer(obj.location).data
        return None
    
    def get_donor_name(self, obj):
        return obj.user.name
    
    def get_phone(self, obj):
        return obj.user.phone
    
    class Meta:
        model = DonorProfile
        fields = "__all__"
        read_only_fields = ("user",)