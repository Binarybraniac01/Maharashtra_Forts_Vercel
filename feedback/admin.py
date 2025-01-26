from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["user", "name","email", "user_feedback", "rating"]
    search_fields = ["user"]

    def name(self, obj):
        user_data_obj = User.objects.get(username=obj.user)
        firstname = user_data_obj.first_name
        lastname = user_data_obj.last_name
        name_ = f"{firstname} {lastname}"
        return name_


admin.site.register(Feedback, FeedbackAdmin)