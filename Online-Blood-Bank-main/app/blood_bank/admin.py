from django.contrib import admin
from .models import BloodRequest,BloodStock,DonorProfile,PatientProfile
# Register your models here.

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("blood_group","quantity", "patient" ,"status")
    list_filter = ("blood_group","patient", "status")
    search_fields =("blood_group","patient","status")

@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ("blood_group","quantity", "donor" ,"status")
    list_filter = ("blood_group","donor", "status")
    search_fields =("blood_group","donor","status")

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ("user","blood_group","location")
    list_filter = ("user","blood_group","location")
    search_fields =("user","blood_group","location")

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("user","blood_group","location")
    list_filter = ("user","blood_group","location")
    search_fields =("user","blood_group","location")