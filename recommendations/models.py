from django.db import models
from django.contrib.auth.models import User



class all_trips(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_trips")
    user_name = models.CharField(max_length=100, null=True, blank=True)
    trip_id = models.AutoField(primary_key=True)
    trip_district = models.CharField(max_length=100,null=True, blank=True)
    forts_visited = models.CharField(max_length=1000, null=True, blank=True)
    required_time = models.CharField(max_length=100, null=True, blank=True)
    minimum_cost = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __repr__(self) :
        return f"({self.trip_id},{self.user},{self.trip_district},{self.forts_visited},{self.required_time},{self.minimum_cost}, {self.date})"

"""
we are making recommedations dynamic based on the districts the user has visited 
- we will get the districts and then get the forts names and store them in variable
- take random 5 to 10 or below length number of forts names and also districts
- we will keep the title, details, image static as its for one distrixct and change the forts and district fileds only
"""

class all_recommendations(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_recommendations")
    recom_district = models.CharField(max_length=50, null=True, blank=True)
    recom_forts = models.CharField(max_length=500, null=True, blank=True)
    recom_title = models.CharField(max_length=200, null=True, blank=True)
    recom_details = models.TextField(null=True, blank=True)
    image_name = models.CharField(max_length=500, null=True, blank=True) 
    date = models.DateField(auto_now_add=True, null=True)

    def __repr__(self) -> str:
        return f"({self.recommendation_id},{self.recom_district},{self.recom_forts},{self.recom_title},{self.recom_details},{self.image_name}, {self.date})"
