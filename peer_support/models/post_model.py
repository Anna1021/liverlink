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
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model options."""
        ordering = ['-created_at']

class PostComment(models.Model):
    """Model for Post Comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.text}'
    
    def get_delete_str(self):
        return self.__str__()