from django.contrib import admin

# Register your models here.
from home.models import *

class Forts_Admin(admin.ModelAdmin):
    list_display = ["fort_id","fort_district", "fort_name", "fort_latitude", "fort_longitude", "fort_image", "link"]
    search_fields = ["fort_district", "fort_name"]

class latitude_longitude_Admin(admin.ModelAdmin):
    list_display = ["user", "plan_id","origin_latitude", "origin_longitude", "destination_latitude", "destination_longitude"]

# class user_location_Admin(admin.ModelAdmin):
#     list_display = ["u_id", "user_latitude", "user_longitude"]

class Route_Admin(admin.ModelAdmin):
    list_display = ["user", "id","origin", "destination", "mode", "traffic_model", "departure_time"]

class Result_Admin(admin.ModelAdmin):
    list_display = ["user", "id","request_time", "origin", "destination", "distance_text", "duration_text", "duration_in_traffic_text"]


class DistMatrix_fort_lat_long_Admin(admin.ModelAdmin):
    list_display = ["matrix_fort_id","matrix_fort_district", "matrix_fort_name", "matrix_fort_latitude", "matrix_fort_longitude"]
    search_fields = ["matrix_fort_district", "matrix_fort_name"]



admin.site.register(Forts, Forts_Admin)
admin.site.register(latitude_longitude, latitude_longitude_Admin)
# admin.site.register(user_location, user_location_Admin)
admin.site.register(Route, Route_Admin)
admin.site.register(Result, Result_Admin)


admin.site.register(DistMatrix_fort_lat_long, DistMatrix_fort_lat_long_Admin)
