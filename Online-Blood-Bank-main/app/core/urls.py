from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('patient/', include('patient.urls')),
    path('donor/', include('donor.urls')),
    path('blood-bank/', include('blood_bank.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
