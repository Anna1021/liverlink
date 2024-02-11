from django.db import models
from .user_model import User

class Notification(models.Model):
    """Model used for notifications."""
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)