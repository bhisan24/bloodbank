from django.contrib import admin
from accounts.models import User
from .models import Address

# Register your models here.
admin.site.register(User)
admin.site.register(Address)


admin.site.site_header = "Mero Sathi"
