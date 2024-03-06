from django.utils import timezone
from django.db import models
from peer_support.models import User

class Post(models.Model):
    """Model for representing text-based posts."""
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Model options."""
        ordering = ['-created_at']

class PostComment(models.Model):
    """Model for Post Comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.text}'
    
    def get_delete_str(self):
        return self.__str__()