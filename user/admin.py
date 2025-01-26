from django.contrib import admin
from .models import *
# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "user_district",
        "curr_lat",
        "curr_log",
    ]

admin.site.register(UserData, UserDataAdmin)
