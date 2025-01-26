from django.contrib import admin
from .models import *
from user.models import *


class all_trips_admin(admin.ModelAdmin):
    list_display = [
        "user_name",
        "trip_id",
        "trip_district",
        "forts_visited",
        "required_time",
        "minimum_cost",
        "date"
    ]
    search_fields = ["user_name"]

    # we could have added filed without affecting the database but it only for view purpose
    # you cannot perform search on them   
    # def name(self, obj):
    #     name_obj =  User.objects.filter(username=obj.user).first()
    #     return name_obj.first_name


class all_recommendations_admin(admin.ModelAdmin):
    list_display = [
        "recommendation_id",
        "user",
        "recom_district",
        "recom_forts",
        "recom_title",
        "recom_details",
        "image_name",
        "date"
    ]
    

admin.site.register(all_trips, all_trips_admin)
admin.site.register(all_recommendations, all_recommendations_admin)