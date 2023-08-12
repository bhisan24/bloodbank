from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.api.managers import UserManager
from core.infrastructure import choices
from core.settings import EMAIL_HOST_USER

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    gender = models.CharField(
        choices=choices.GENDER_TYPES, max_length=10, default=choices.MALE
    )
    role = models.CharField(
        choices=choices.PROFILE_TYPES, max_length=15, default=choices.PATIENT
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Address(models.Model):
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    local_body_name = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.address


class UserToken(models.Model):
    """Database Table for User Tokens Generated to Reset Password"""
    
    email = models.EmailField(max_length=255)
    token = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.email


def send_password_reset_email(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'RESET PASSWORD'
        message = f'http://127.0.0.1:8000/accounts/reset-password/?token={instance.token}'
        from_email = EMAIL_HOST_USER
        to_email = [instance.email]
        send_mail(subject,message,from_email,to_email)

post_save.connect(send_password_reset_email, sender=UserToken)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")