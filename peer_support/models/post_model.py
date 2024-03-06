from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.db import models
#post 
from peer_support.models import User
from django.core.validators import RegexValidator

class Post(models.Model):
    """Model for representing text-based posts."""
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #title = models.CharField(max_length=100)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Model options."""
        ordering = ['-created_at']

    def get_comments(self):
        """Return comments"""
        return self.replies.filter(parent=None)
