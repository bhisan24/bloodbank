from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail

from core.settings import EMAIL_HOST_USER
from core.infrastructure import choices
from donor.models import DonorProfile
from patient.models import PatientProfile


class BloodStock(models.Model):
    """Database model for Bloods Donated by Donors"""
    
    blood_group = models.CharField(
        choices=choices.BLOOD_GROUP_TYPES, max_length=5
    )
    quantity = models.IntegerField()
    donor = models.ForeignKey(DonorProfile, related_name="blood_donor", on_delete=models.CASCADE)
    status = models.CharField(
        choices=choices.REQUEST_STATUS, max_length=20, default=choices.PENDING
    )
    
    def __str__(self):
        return "Stock " + self.blood_group + " " + str(self.quantity)


class BloodRequest(models.Model):
    """Database model for Blood Requests by Patients"""
    
    blood_group = models.CharField(
        choices=choices.BLOOD_GROUP_TYPES, max_length=5
    )
    quantity = models.IntegerField()
    patient = models.ForeignKey(PatientProfile, related_name="request_user", on_delete=models.CASCADE)
    status = models.CharField(
        choices=choices.REQUEST_STATUS, max_length=20, default=choices.PENDING
    )
    
    def __str__(self):
        return "Request " + self.blood_group + " " + str(self.quantity)


def notify_donor_on_request(sender, instance, created, *args, **kwargs):
    """function to notify donors if requested blood is not available on stock"""
    requested_blood_group_stock = BloodStock.objects.filter(blood_group=instance.blood_group, status="PENDING")
    if created and not requested_blood_group_stock.count():
        requested_blood_group_donor_emails = list(
            DonorProfile.objects.filter(blood_group=instance.blood_group).values_list(
                "user__email", flat=True
            )
        )
        send_mail(
            "BLOOD REQUIRED",
            f"{instance.quantity} pints {instance.blood_group} blood required. Please Donate if possible.",
            EMAIL_HOST_USER,
            requested_blood_group_donor_emails,
        )

post_save.connect(notify_donor_on_request, sender=BloodRequest)