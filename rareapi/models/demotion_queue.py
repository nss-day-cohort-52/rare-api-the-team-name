from django.db import models

class DemotionQueue(models.Model):
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='demote_admin')
    requester = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='demote_requester')