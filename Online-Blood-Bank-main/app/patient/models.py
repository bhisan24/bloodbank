from django.db import models
from django.db.models.signals import post_save

import uuid
import os

from accounts.models import User, Address
from core.infrastructure import choices


def get_patient_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join("uploads/patient_images/", filename)


class PatientProfile(models.Model):
    """Database model for Patient Profile in the system"""
    
    user = models.OneToOneField(User, related_name="patient_profile", on_delete=models.CASCADE)
    blood_group = models.CharField(
        choices=choices.BLOOD_GROUP_TYPES, max_length=5
    )
    image = models.ImageField(upload_to=get_patient_image_filename, blank=True, null=True)
    location = models.ForeignKey(Address, related_name="patient_address", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.name


def add_patient_profile(sender, instance, *args, **kwargs):
    if instance.role == choices.PATIENT and not PatientProfile.objects.filter(user=instance).exists():
        PatientProfile.objects.create(user=instance)

post_save.connect(add_patient_profile, sender=User)
