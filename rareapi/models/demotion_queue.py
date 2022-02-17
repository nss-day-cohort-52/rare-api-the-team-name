from django.db import models

class DemotionQueue(models.Model):
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='admin')
    requester = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='requester')