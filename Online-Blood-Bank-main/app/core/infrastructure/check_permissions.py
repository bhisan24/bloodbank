from rest_framework import permissions

from core.infrastructure.choices import ADMIN, PATIENT, DONOR


class PatientProfilePermissions(permissions.BasePermission):
    """Only Allow Patients to Access and Manage their Own Profile"""
    
    def has_permission(self, request, view):
        return request.user.role == PATIENT
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class DonorProfilePermissions(permissions.BasePermission):
    """Only Allow Donors to Access and Manage their Own Profile"""
    
    def has_permission(self, request, view):
        return request.user.role == DONOR
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class OwnProfilePermissions(permissions.BasePermission):
    """Only Allow Users to Manage their own Profile"""
    
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class BloodStockPermissions(permissions.BasePermission):
    """Only Allow Donors and Admin to Access and Manage their Own Donations"""
    
    def has_permission(self, request, view):
        return request.user.role in [DONOR, ADMIN]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == ADMIN:
            return True
        return obj.donor == request.user.donor_profile


class BloodRequestPermissions(permissions.BasePermission):
    """Only Allow Patient and Admin to Access and Manage their Own Requests"""
    
    def has_permission(self, request, view):
        return request.user.role in [PATIENT, ADMIN]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == ADMIN:
            return True
        return obj.patient == request.user.patient_profile


class IsTokenValid(permissions.BasePermission):
    def has_permission(self, request, view):
        from accounts.models import BlackListedToken
        
        user_id = request.user.id            
        is_allowed_user = True
        token = request.auth
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user