from urllib import response
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from uuid import uuid4

from accounts.api import serializers
from accounts.models import User, Address, UserToken
from core.infrastructure import choices, check_permissions
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterPatientView(viewsets.ModelViewSet):
    """API Views for Registering Patients in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.PATIENT)


class RegisterDonorView(viewsets.ModelViewSet):
    """API Views for Registering Donors in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.DONOR)


class CustomAdminLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomAdminOnlyJWTToken


class CustomDonorLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomDonorOnlyJWTToken


class CustomPatientLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomPatientOnlyJWTToken


class CustomRefreshView(TokenObtainPairView):
    
    serializer_class = serializers.CustomRefreshJWTToken


class UserProfileView(viewsets.ModelViewSet):
    """API Views for Handling User Profile in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, check_permissions.OwnProfilePermissions, check_permissions.IsTokenValid)
    http_method_names = ["get","put","patch","delete"]
    
    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)


class AddressViewSet(viewsets.ModelViewSet):
    """API Views for Handling  Gym Address in the System"""
    
    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (IsAuthenticated, check_permissions.IsTokenValid)


class ForgetPasswordView(APIView):
    """API View for Forget Password"""
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        # getting email from request body
        email = self.request.data.get("email", None)
        # validating if user has entered email and email for registered user exists
        if email and User.objects.filter(email=email).exists():
            # creating token in database for user
            UserToken.objects.create(email=email,token=uuid4())
            # returning success response to the user
            return Response("Password reset link sent successfully. Please check email", status=status.HTTP_200_OK)
        else:
            # returning error response to the user if email is not entered or does not exist
            return Response("Please enter registered email", status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """API View for resetting password"""
    permission_classes = (AllowAny,)
    def get(self, request):
        return render(request, 'forgetPassword.html')
    
    def post(self, request, format=None):
        # getting token from url
        token = self.request.query_params.get("token", None)
        user_token = UserToken.objects.filter(token=token).first()
        # validating if token exists
        if user_token:
            user = User.objects.get(email=user_token.email)
            # getting password and confirm password from request body
            password = self.request.data.get("password", None)
            confirm_password = self.request.data.get("confirm_password", None)
            # changing password if both match
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return Response("Password changed successfully.", status=status.HTTP_200_OK)
            else:
                return Response("Password and Confirm Password do not match", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No token exists in DB for user Please Try Again", status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LogoutSerializer
    http_method_names = ["post"]
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response("Already Logged Out", status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)