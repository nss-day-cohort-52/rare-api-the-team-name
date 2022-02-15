from django.db import models

class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    
    @property
    def ended_on(self):
        return self.__ended_on

    @ended_on.setter
    def ended_on(self, date):
        """date subscription ended"""
        self.__ended_on = date