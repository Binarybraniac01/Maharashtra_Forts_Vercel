from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_feedback")
    email = models.EmailField(null=True, blank=True)
    user_feedback = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
