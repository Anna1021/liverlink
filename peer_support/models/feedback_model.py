from django.db import models

class Feedback(models.Model):
    """Model used for storing user feedback."""
    title = models.CharField(max_length=50, blank=False)
    content = models.CharField(max_length=500, blank=False)
    submitted_at = models.DateTimeField(auto_now_add=True)