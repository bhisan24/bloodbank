
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from core.infrastructure.choices import ADMIN, DONOR, PATIENT
from accounts.models import User, Address, BlackListedToken


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User database object"""

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "name",
            "address",
            "gender",
            "phone",
            "password",
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CustomRefreshJWTToken(TokenRefreshSerializer):
    
    def validate(self,attrs):
        data = super().validate(attrs)
        if not RefreshToken(attrs['refresh']):
            raise serializers.ValidationError("Refresh token is undefined", 405)
        user_id = RefreshToken(attrs['refresh']).access_token['user_id']
        if user_id:
            user = User.objects.get(pk=user_id)
            data['user_id'] = user.id
            data['name'] = user.name
        return data


class CustomAdminOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != ADMIN:
            raise serializers.ValidationError("Only Admin is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        return data


class CustomDonorOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != DONOR:
            raise serializers.ValidationError("Only Donor is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        return data


class CustomPatientOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != PATIENT:
            raise serializers.ValidationError("Only Patient is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        return data


class AddressSerializer(serializers.ModelSerializer):
    """Serializes Address Object"""
    
    class Meta:
        model = Address
        fields = "__all__"
    
    def validate(self, attrs):
        latitude = attrs.get("latitude", None)
        longitude = attrs.get("longitude", None)
        if not latitude or not longitude:
            raise serializers.ValidationError("Latitude and Longitude cannot be null", 400)
        return super().validate(attrs)


class LogoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlackListedToken
        fields = ("token",)