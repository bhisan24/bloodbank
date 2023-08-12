from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts import models as accounts_models
from donor import models as donor_models
from patient import models as patient_models


def sample_user(email='test@testing.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@mytestapp.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests the email for new user is normalized"""
        email = 'test@MYTESTAPP.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@testing.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_address_created(self):
        """Test creating address"""
        address = accounts_models.Address.objects.create(address="thamel")
        self.assertEqual(address.address, "thamel")
    
    def test_create_donor_role_creates_profile(self):
        """Test creating user with donor role creates Donor Profile Automatically"""
        
        donor = accounts_models.User.objects.create(email="testdonor@email.com", name="test donor", address="test address", phone="9800515353", role="DONOR")
        donor_profile = donor_models.DonorProfile.objects.filter(user__email=donor.email).exists()
        self.assertTrue(donor_profile)
    
    def test_create_patient_role_creates_profile(self):
        """Test creating user with patient role creates patient Profile Automatically"""
        
        patient = accounts_models.User.objects.create(email="testpatient@email.com", name="test patient", address="test address", phone="9800515353", role="PATIENT")
        patient_profile = patient_models.PatientProfile.objects.filter(user__email=patient.email).exists()
        self.assertTrue(patient_profile)