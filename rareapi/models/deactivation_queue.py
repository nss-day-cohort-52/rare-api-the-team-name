from django.db import models


class DeactivationQueue(models.Model):
    admin = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name='deactivate_admin')
    requester = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name='deactivate_requester')
