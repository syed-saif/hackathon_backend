import os
from django.conf import settings
from django.db import models

class DetecHandWritten(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='detect_images/', null=True, blank=True)
    result = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=255, default="new")
    is_correct = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detect_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detect_updated_by')
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'