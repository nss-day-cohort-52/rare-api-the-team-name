from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250)
    profile_image_url = models.URLField(max_length=500)
    following = models.ManyToManyField('RareUser', through='Subscription', symmetrical=False, related_name="followers")
    active = models.BooleanField(default=True)


# created_on = models.DateField(auto_now_add=True)
