from django.utils import timezone
from django.db import models
from peer_support.models import User

class Post(models.Model):
    """Model for representing text-based posts."""
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    visibility = models.CharField(default='G',max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Model options."""
        ordering = ['-created_at']

    def get_comments(self):
        """Return comments"""
        return self.replies.filter(parent=None)
