from django.contrib import admin
from .models import CustomUser, Decedent

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Decedent)
