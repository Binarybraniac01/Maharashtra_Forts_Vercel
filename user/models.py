from django.db import models
from django.contrib.auth.models import User


"""
we can integrate user login and store each users dis and location and its trips info
To achieve this
- create model
- add login auth to website and add code to check if thats the same user then update the location and dist info
- afterwards also add all the trips that this user 
"""

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_data")
    user_district = models.CharField(max_length=100, null=True)
    curr_lat = models.FloatField(null=True, blank=True)
    curr_log = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user_district


